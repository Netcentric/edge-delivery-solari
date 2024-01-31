import clsx from 'clsx';
import { ReactComponent as ArrowRightBoldSVG } from '../../assets/icons/arrow-right-bold.svg';

const IconComponents = {
  ArrowRightBold: ArrowRightBoldSVG,
};

export type Icon = keyof typeof IconComponents;

export interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'link';
  size?: 'default' | 'small' | 'large' | 'tiny';
  label?: string;
  iconLeft?: Icon;
  iconRight?: Icon;
}

const common = 'font-gellix flex items-center gap-1 rounded-full font-semibold disabled:opacity-25';
const defaultSize = 'text-xl leading-5 py-3.5 px-6';
const small = 'leading-4 px-5 py-3';
const large = 'text-2xl leading-6 px-8 py-4.5';
const tiny = 'text-xs leading-3 px-3.5 py-2';

const primary =
  'bg-dark-teal text-midnight-blue hover:bg-medium-teal active:bg-light-teal focus:outline focus:outline-2 focus:outline-offset-1 focus:outline-link-blue';
const secondary =
  'btn-secondary border-2 border-link-blue border-solid text-link-blue hover:text-midnight-blue hover:border-midnight-blue focus:outline focus:outline-2 focus:outline-offset-1 focus:outline-link-blue';
const link = `${secondary} !p-0 !border-none focus:!outline-none`;

export const Button = ({
  variant = 'primary',
  size = 'default',
  label,
  iconRight,
  iconLeft,
  disabled,
  ...props
}: ButtonProps) => {
  const IconLeft = iconLeft && IconComponents[iconLeft];
  const IconRight = iconRight && IconComponents[iconRight];
  return (
    <button
      className={clsx(common, {
        [defaultSize]: size === 'default',
        [small]: size === 'small',
        [large]: size === 'large',
        [tiny]: size === 'tiny',
        [primary]: variant === 'primary',
        [secondary]: variant === 'secondary',
        [link]: variant === 'link',
      })}
      disabled={disabled}
      {...props}
    >
      {IconLeft && (
        <IconLeft
          className={clsx({
            'size-5': size === 'default',
            'size-4': size === 'small',
            'size-6': size === 'large',
            'size-3': size === 'tiny',
          })}
        />
      )}
      {label}
      {IconRight && (
        <IconRight
          className={clsx({
            'size-5': size === 'default',
            'size-4': size === 'small',
            'size-6': size === 'large',
            'size-3': size === 'tiny',
          })}
        />
      )}
    </button>
  );
};
