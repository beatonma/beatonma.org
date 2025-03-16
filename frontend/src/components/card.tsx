// import { ReactNode } from "react";
// import { DivProps, DivPropsNoChildren } from "@/types/react";
// import { onlyIf } from "@/util/optional";
// import { addClass } from "@/util/transforms";
//
// interface CardProps {
//   image?: ReactNode;
// }
//
// export default function Card(props: CardProps & DivProps) {
//   const { image, children, ...rest } = addClass(
//     props,
//     "card @container row gap-2",
//   );
//   return (
//     <div {...rest}>
//       {onlyIf(image, <div>{image}</div>)}
//       <div className="column">{children}</div>
//     </div>
//   );
// }
