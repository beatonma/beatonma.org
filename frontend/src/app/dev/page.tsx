import { Metadata } from "next";
import { Row } from "@/components/layout";
import * as Preview from "./_components";

export const metadata: Metadata = {
  title: "Components overview",
  description: "",
};

export default function Page() {
  return (
    <>
      <Row className="justify-between w-full">
        <h1>Components overview</h1>
      </Row>
      <Preview.Buttons />
      <Preview.Icons />
      <Preview.Callouts />
      <Preview.Loaders />
    </>
  );
}
