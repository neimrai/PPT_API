import * as z from "zod";
// Note:
// If you want to use images and icons, you must use ImageSchema and IconSchema
// Images and icons are the only media types supported for PDF and PPTX exports
import {
  ImageSchema,
  IconSchema,
} from "@/presentation-templates/defaultSchemes";

// Schema definition
export const Schema = z.object({
  // Notes:
  // Schema fields
  // Each field must have a default value (this is important for Layout Preview)
  // Each field must have a meta description
  // Each field must have a minimum and maximum length
  // Each array field must have a minimum and maximum number of items
  title: z.string().min(3).max(50).default("Slide Layout Title").meta({
    description: "Main title of the slide",
  }),
  description: z
    .string()
    .min(10)
    .max(180)
    .default("Slide Layout Description")
    .meta({
      description: "Content description of the slide",
    }),
});

// Type inference
type SchemaType = z.infer<typeof Schema>;

// Component definition
const SlideComponent = ({ data }: { data: Partial<SchemaType> }) => {
  // Notes:
  // Must have consistent aspect ratio (16:9) and max-width of 1280px.
  // Validate each data field before rendering using && operator or optional chaining.
  // These layouts are exported as PDF and PPTX so they must be optimized for both formats.
  // Content must properly fit in the container, specify min and max constraints in the schema.
  // You can check out ExampleSlideLayout.tsx for more details.
  return (
    <div className="h-full w-full flex flex-col justify-center items-center p-10">
      <h1 className="text-4xl font-bold">{data.title}</h1>
      <p className="mt-6">{data.description}</p>
    </div>
  );
};

export default SlideComponent;
