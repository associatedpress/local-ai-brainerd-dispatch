import React, { useState } from 'react';
import './Banner.css';

const Banner = ({ message, isVisible, onClose, isSuccess }) => {
  const bannerClass = isSuccess ? 'banner banner-success' : 'banner banner-error';

  return (
    <div className={`banner ${bannerClass}`}>
      <div className="message">{message}</div>
      <button className="close-button" onClick={onClose}>X</button>
    </div>
  );
};

export default Banner;
