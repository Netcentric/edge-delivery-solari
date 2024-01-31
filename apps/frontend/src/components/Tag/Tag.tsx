import React from 'react';
import vector from '../../assets/icons/vector.svg';
import clsx from 'clsx';

interface TagProps {
  label: string;
  isSelected?: boolean;
}

export const Tag = ({ label, isSelected }: TagProps) => {
    const [selected, setSelected] = React.useState<boolean>(isSelected || false);

  const commonClasses = 'rounded-[2.5rem] font-gellix text-[1.25rem] leading-5 p-[1.875rem]';

  const handleClick = ()=> {
    setSelected(!selected);
  }

  return (
    <div className={clsx(commonClasses,{
        'flex bg-midnight-blue text-white': selected === true,
        'text-midnight-blue border border-midnight-blue hover:bg-midnight-blue hover:text-white': selected === false
    })} onClick={handleClick}>
      {label}
      {selected && <img className='pl-[1.125rem]' src={vector} alt="logo" />}
    </div>
  );
};
