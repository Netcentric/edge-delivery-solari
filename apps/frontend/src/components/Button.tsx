export interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'link';
  size?: 'default' | 'small' | 'large' | 'tiny';
  label: string;
}

export const Button = ({ variant = 'primary', size = 'default', onClick, label, ...props }: ButtonProps) => {
  return <button onClick={onClick}>{label}</button>;
};
