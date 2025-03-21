import { Row } from "@/components/layout";
import ThemeController from "@/components/themed/light-dark";
import * as Preview from "./_components";

export default function Page() {
  return (
    <main className="mx-auto column gap-16 mb-16 items-center">
      <div className="readable space-y-16">
        <Row className="justify-between w-full">
          <h1>Components overview</h1>
          <ThemeController />
        </Row>
        <Preview.Buttons />
        <Preview.Icons />
        <Preview.Loaders />
        <Preview.Media />
      </div>
    </main>
  );
}
