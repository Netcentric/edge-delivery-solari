import React from 'react';
import vector from '../../assets/icons/vector.svg';
import clsx from 'clsx';

interface TagProps {
  label: string;
  isSelected?: boolean;
  onClick: () => void;
}

export const Tag = ({ label, isSelected, onClick }: TagProps) => {
    const [selected, setSelected] = React.useState<boolean>(isSelected || false);

  const commonClasses = 'rounded-full font-gellix font-semibold text-xl leading-5 px-[1.875rem] py-[0.938rem] border ';

  const handleClick = ()=> {
    setSelected(selected => !selected);
    onClick();
  }

  return (
    <button className={clsx(commonClasses,{
        'flex bg-midnight-blue text-white': selected === true,
        'text-midnight-blue border-midnight-blue hover:bg-midnight-blue hover:text-white': selected === false
    })} onClick={handleClick}>
      {label}
      {selected && <img className='pl-[1.125rem] pt-[0.313rem]' src={vector} alt="cancel" />}
    </button>
  );
};
