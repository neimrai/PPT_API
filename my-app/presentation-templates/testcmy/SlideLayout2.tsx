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
  image: ImageSchema.default({
    __image_url__:
      "https://cdn.pixabay.com/photo/2015/12/01/20/28/road-1072823_1280.jpg",
    __image_prompt__: "A beautiful road in the mountains",
  }).meta({
    description: "Image to display in the slide",
  }),
  icon: IconSchema.default({
    __icon_url__: "/static/icons/placeholder.png",
    __icon_query__: "A beautiful road in the mountains",
  }).meta({
    description: "Icon to display in the slide",
  }),
});

// Type inference
type SchemaType = z.infer<typeof Schema>;

// Component definition
const SlideComponent = ({ data }: { data: Partial<SchemaType> }) => {
  return (
    <div className="h-full w-full flex justify-center items-center gap-4 p-10">
      <div className="basis-1/2 rounded-lg overflow-hidden">
        <img
          className="w-full"
          src={data.image?.__image_url__}
          alt={data.image?.__image_prompt__}
        />
      </div>
      <div className="basis-1/2 flex flex-col justify-center items-center">
        <img
          className="w-16 h-16"
          src={data.icon?.__icon_url__}
          alt={data.icon?.__icon_query__}
        />
        <h1 className="mt-4 text-4xl font-bold">{data.title}</h1>
        <p className="mt-6">{data.description}</p>
      </div>
    </div>
  );
};

export default SlideComponent;
