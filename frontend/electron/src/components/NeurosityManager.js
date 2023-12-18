import React, { useState, useEffect } from 'react';
import { useNotion } from '../services/notion';

export default function NeurosityManager() {
  const { notion } = useNotion();
  const [brainData, setBrainData] = useState([]);
  const [deviceInfo, setDeviceInfo] = useState(null);

  useEffect(() => {
    const getDeviceInfo = async () => {
      const info = await notion.getInfo();
      setDeviceInfo(info);
    };

    const brainwavesCallback = (data) => {
      if (data) {
        const timestamp = new Date().toISOString();
        setBrainData(prevData => [...prevData, { data, timestamp }]);
        console.log('Wrote line to brainData');
      } else {
        console.log('Received data is None');
      }
    };

    const startBrainwavesCollection = () => {
      notion.brainwaves("raw").subscribe(brainwavesCallback);
    };

    const stopBrainwavesCollection = () => {
      notion.brainwaves("raw").unsubscribe(brainwavesCallback);
    };

    if (notion) {
      startBrainwavesCollection();
      getDeviceInfo();
    }
    return () => {
      if (notion) {
        stopBrainwavesCollection();
      }
    };
  }, [notion]);

  return (
    <div>
      <pre>{deviceInfo ? JSON.stringify(deviceInfo, null, 2) : 'No device info'}</pre>
      <pre>{brainData.length > 0 ? JSON.stringify(brainData, null, 2) : 'No brain data'}</pre>
    </div>
  );
};