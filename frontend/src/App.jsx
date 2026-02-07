/**
 * Main App component
 * Orchestrates the campaign form and list
 */

import React, { useState } from 'react';
import Layout from './components/Layout';
import CampaignForm from './components/CampaignForm';
import CampaignList from './components/CampaignList';

function App() {
  const [refreshTrigger, setRefreshTrigger] = useState(0);

  const handleCampaignCreated = () => {
    // Trigger refresh of campaign list
    setRefreshTrigger((prev) => prev + 1);
  };

  return (
    <Layout>
      <CampaignForm onSuccess={handleCampaignCreated} />
      <CampaignList refreshTrigger={refreshTrigger} />
    </Layout>
  );
}

export default App;
