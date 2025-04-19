import { ReactNode, useId } from "react";

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
