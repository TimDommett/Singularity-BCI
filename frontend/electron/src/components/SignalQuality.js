// frontend/my-electron-app/src/components/SignalQuality.js

import React from 'react';

const SignalQuality = ({ signalQuality }) => {
    return (
        <div>
            <h2>Signal Quality</h2>
            <p>{signalQuality}</p>
        </div>
    );
};

export default SignalQuality;