import React from 'react';
import vector from '../../assets/icons/vector.svg';

interface TagProps {
  label: string;
  isSelected?: boolean;
}

export const Tag = ({ label, isSelected }: TagProps) => {
    const [selected, setSelected] = React.useState<boolean>(isSelected || false);

  const classes = 'rounded-[40px] font-gellix text-[20px] leading-5 p-[30px] '.concat(
    selected === true ? 'flex bg-midnight-blue text-white' : 'text-midnight-blue border border-midnight-blue hover:bg-midnight-blue hover:text-white',
  );

  const handleClick = ()=> {
    setSelected(!selected);
  }

  return (
    <div className={classes} onClick={handleClick}>
      {label}
      {selected && <img className='pl-[18px]' src={vector} alt="logo" />}
    </div>
  );
};
