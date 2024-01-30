import clsx from 'clsx';

type Icon = React.FunctionComponent<
  React.SVGProps<SVGSVGElement> & {
    title?: string | undefined;
  }
>;

export interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'link';
  size?: 'default' | 'small' | 'large' | 'tiny';
  label: string;
  /**
   * import { ReactComponent as YourIcon } from '/assets/icons/...svg
   */
  IconLeft?: Icon;
  /**
   * import { ReactComponent as YourIcon } from '/assets/icons/...svg
   */
  IconRight?: Icon;
}

const common = 'btn font-gellix flex items-center gap-5px rounded-full font-semibold disabled:opacity-25';
const defaultSize = 'text-xl leading-5 py-15px px-25px';
const small = 'leading-4 px-5 py-3';
const large = 'text-25px leading-25px px-31.25px py-18.75px';
const tiny = 'text-xs leading-3 px-15px py-9px';

const primary =
  'bg-dark-teal text-midnight-blue hover:bg-medium-teal active:bg-light-teal focus:outline focus:outline-2 focus:outline-offset-1 focus:outline-link-blue';
const secondary =
  'btn-secondary border-2 border-link-blue border-solid text-link-blue hover:text-midnight-blue hover:border-midnight-blue focus:outline focus:outline-2 focus:outline-offset-1 focus:outline-link-blue';
const link = `${secondary} !p-0 !border-none focus:!outline-none`;

export const Button = ({
  variant = 'primary',
  size = 'default',
  onClick,
  label,
  IconRight,
  IconLeft,
  disabled,
  ...props
}: ButtonProps) => {
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
            'size-25px': size === 'large',
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
            'size-25px': size === 'large',
            'size-3': size === 'tiny',
          })}
        />
      )}
    </button>
  );
};
