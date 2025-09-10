const fs = require("fs");
const path = require("path");
const Babel = require("@babel/standalone");
const z = require("zod");
const recharts = require("recharts");
/**
 * Compile TypeScript/TSX code to extract layout information.
 * @param {string} layoutCode - The TypeScript/TSX code of the layout.
 * @returns {Object} Extracted layout information.
 */
const compileLayout = (layoutCode) => {
  const cleanCode = layoutCode
    .replace(/import\s+.*\s+from\s+['"].*['"];?/g, "") // 移除所有 import 语句
    .replace(/export\s+(const|default|type|interface)\s+/g, "") // 移除所有 export 语法
    .replace(/export\s*{\s*.*\s*};?/g, "") // 移除导出的对象语法
    .replace(/typescript/g, ""); // 移除 TypeScript 特有语法

  // 打印清理后的代码
  // console.log("Cleaned Code:\n", cleanCode);

  const compiled = Babel.transform(cleanCode, {
    presets: [
      ["react", { runtime: "classic" }],
      ["typescript", { isTSX: true, allExtensions: true }],
    ],
    sourceType: "script",
  }).code;

  const factory = new Function(
    "React",
    "_z",
    "Recharts",
    `
    const z = _z;
    const ImageSchema = z.object({ __image_url__: z.string(), __image_prompt__: z.string() });
    // 暴露常用的Recharts组件给编译后的布局
    const { ResponsiveContainer, LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, PieChart, Pie, Cell, AreaChart, Area, RadarChart, Radar, PolarGrid, PolarAngleAxis, PolarRadiusAxis } = Recharts || {};
      ${compiled}

      /* 字符串中声明的所有内容在这里都是可访问的 */
      return {
        __esModule: true,   
        default: typeof dynamicSlideLayout !== 'undefined' ? dynamicSlideLayout : (typeof DefaultLayout !== 'undefined' ? DefaultLayout : undefined),
        layoutName,
        layoutId,
        layoutDescription,
        Schema
      };
    `
  );

  return factory({}, z, recharts);
};

/**
 * Extract layout information from a file.
 * @param {string} filePath - Path to the layout file.
 * @returns {Object} Extracted layout information.
 */
const extractLayoutInfo = (filePath) => {
  const layoutCode = fs.readFileSync(filePath, "utf-8");
  const module = compileLayout(layoutCode);

  if (!module.layoutId || !module.layoutName || !module.Schema) {
    throw new Error(`Invalid layout file: ${filePath}`);
  }

  const jsonSchema = z.toJSONSchema(module.Schema, {
    override: (ctx) => {
      delete ctx.jsonSchema.default;
    },
  });

  return {
    id: module.layoutId,
    name: module.layoutName,
    description: module.layoutDescription || `${module.layoutName} layout`,
    json_schema: jsonSchema,
  };
};

/**
 * Process all layout files in a directory.
 * @param {string} dirPath - Path to the directory containing layout files.
 * @returns {Object[]} Array of extracted layout information.
 */
const processLayouts = (dirPath) => {
  const files = fs.readdirSync(dirPath);
  const layouts = [];

  files.forEach((file) => {
    if (file.endsWith(".tsx") || file.endsWith(".ts")) {
      const filePath = path.join(dirPath, file);
      try {
        const layoutInfo = extractLayoutInfo(filePath);
        console.log(`Processed layout: ${layoutInfo.name}`);
        layouts.push(layoutInfo);
      } catch (error) {
        console.error(`Error processing file ${file}:`, error.message);
      }
    }
  });

  return layouts;
};

// Example usage
const layoutDir = path.resolve(
  __dirname,
  "../../../my-presentation-app/presentation-templates/classic"
);
const layouts = processLayouts(layoutDir);
console.log("Extracted Layouts:", layouts);
console.log("Extracted Layouts:", JSON.stringify(layouts, null, 2));
