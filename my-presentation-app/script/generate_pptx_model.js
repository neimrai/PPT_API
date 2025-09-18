// generate_pptx_model.js
import {
  getBrowserAndPage,
  getSlidesAndSpeakerNotes,
  getAllChildElementsAttributes,
  postProcessSlidesAttributes,
} from "../app/api/presentation_to_pptx_model/route.ts";
import { convertElementAttributesToPptxSlides } from "../utils/pptx_models_utils.ts";

async function generatePptxModel(presentationId) {
  if (!presentationId) {
    throw new Error("Presentation ID is required");
  }

  try {
    // 1. 初始化浏览器和页面
    const [browser, page] = await getBrowserAndPage(presentationId);

    try {
      // 2. 获取幻灯片内容和演讲者注释
      const { slides, speakerNotes } = await getSlidesAndSpeakerNotes(page);

      // 3. 获取所有子元素的属性
      const slidesAttributes = [];
      for (const slide of slides) {
        const attributes = await getAllChildElementsAttributes(slide);
        slidesAttributes.push(attributes);
      }

      // 4. 后处理幻灯片属性
      const processedAttributes = await postProcessSlidesAttributes(
        slidesAttributes
      );

      // 5. 转换元素属性为PPTX幻灯片模型
      const pptxSlides = await convertElementAttributesToPptxSlides(
        processedAttributes
      );

      // 6. 构建完整的演示文稿模型
      const presentation_pptx_model = {
        name: `Presentation-${presentationId}`,
        slides: pptxSlides.map((slide, index) => ({
          ...slide,
          speakerNote: speakerNotes[index] || "",
        })),
      };

      // 7. 关闭浏览器
      await browser.close();

      return presentation_pptx_model;
    } catch (error) {
      // 确保在出错时也关闭浏览器
      await browser.close();
      throw error;
    }
  } catch (error) {
    console.error("Error generating PPTX model:", error);
    throw error;
  }
}

// 命令行参数验证
if (process.argv.length < 3) {
  console.error("Usage: node generate_pptx_model.js <presentationId>");
  process.exit(1);
}

// 命令行调用
// const presentationId = process.argv[2];
// generatePptxModel(presentationId)
//   .then((result) => {
//     // 将结果输出为JSON字符串，保持格式化以提高可读性
//     console.log(JSON.stringify(result, null, 2));
//   })
//   .catch((error) => {
//     console.error("Failed to generate PPTX model:", error);
//     process.exit(1);
//   });

const presentationId = "";
generatePptxModel(presentationId)
  .then((result) => {
    console.log("Generated PPTX Model:", JSON.stringify(result, null, 2));
  })
  .catch((error) => {
    console.error("Failed to generate PPTX model:", error);
  });
