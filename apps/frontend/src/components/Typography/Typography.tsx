import clsx from 'clsx';

export interface HeadingProps {
  level: 'h1' | 'h2' | 'h3' | 'h4' | 'h5';
  children: React.ReactNode;
}
const common = 'font-gellix';
const h1 = 'text-6xl font-semibold leading-[4.25rem]';
const h2 = 'text-5xl font-semibold leading-[3.5rem]';
const h3 = 'text-4xl font-semibold leading-[2.75rem]';
const h4 = 'text-3xl font-light';
const h5 = 'text-2xl';

export const Heading = ({ level, children }: HeadingProps) => {
  const Tag = level;

  return (
    <Tag
      className={clsx(common, {
        [h1]: level === 'h1',
        [h2]: level === 'h2',
        [h3]: level === 'h3',
        [h4]: level === 'h4',
        [h5]: level === 'h5',
      })}
    >
      {children}
    </Tag>
  );
};

export interface TextProps {
  size?: 'default' | 'small' | 'tiny';
  weight?: 'regular' | 'bold';
  children: React.ReactNode;
}

export const Text = ({ size = 'default', weight = 'regular', children }: TextProps) => {
  return (
    <p
      className={clsx(common, {
        'font-semibold': weight === 'bold',
        'text-[1.25rem] leading-6': size === 'default',
        'text-sm leading-5': size === 'small',
        'text-xs leading-4': size === 'tiny',
      })}
    >
      {children}
    </p>
  );
};
