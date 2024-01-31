import React from 'react';
import logo from '../../assets/icons/logo.svg';
import wordmark from '../../assets/icons/wordmark-cognizant.svg';

export const Header = () => (
  <header>
    <div className="flex justify-between mx-12 py-[18px]">
      <div className='flex'>
        <img src={logo} alt="logo" />
        <img src={wordmark} alt="wordmark" />
      </div>
      <div>
        <span className='font-gellix text-midnight-blue text-[20px] leading-5 font-semibold'>Solari Astrocraft</span>
      </div>
    </div>
  </header>
);
