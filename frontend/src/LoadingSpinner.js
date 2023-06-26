import React from 'react';
import hourglass from './assets/Hourglass.gif';

function Spinner() {
  return (
    <div>
      <img
        src={hourglass}
        style={{ width: '100px', margin: "32px auto 32px auto", display: 'block' }}
        alt="Loading..."
      />
    </div>
  );
};

export default Spinner;