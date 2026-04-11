import { ReactNode, useId } from "react";
import { Row } from "@/components/layout";
import { DivProps, StateSetter } from "@/types/react";
import { addClass } from "@/util/transforms";

export const FormField = (props: {
  label: string;
  block: (id: string) => ReactNode;
}) => {
  const { label, block } = props;
  const id = useId();
  return (
    <p>
      <label className="block mb-1" htmlFor={id}>
        {label}
      </label>

      {block(id)}
    </p>
  );
};

export const CheckBox = (
  props: DivProps<{
    isChecked: boolean;
    setChecked: StateSetter<boolean>;
    label: string;
  }>,
) => {
  const { isChecked, setChecked, label, ...rest } = props;
  const id = useId();

  return (
    <Row {...addClass(rest, "gap-x-2")}>
      <input
        id={id}
        type="checkbox"
        checked={isChecked}
        onChange={(ev) => setChecked(ev.target.checked)}
      />
      <label htmlFor={id}>{label}</label>
    </Row>
  );
};
