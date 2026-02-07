/**
 * CampaignList component
 * Displays all campaigns with actions for publish and disable
 */

import React, { useState, useEffect } from 'react';
import { campaignAPI } from '../services/api';

const CampaignList = ({ refreshTrigger }) => {
  const [campaigns, setCampaigns] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [actionLoading, setActionLoading] = useState({});
  const [actionMessages, setActionMessages] = useState({});

  useEffect(() => {
    fetchCampaigns();
  }, [refreshTrigger]);

  const fetchCampaigns = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await campaignAPI.getAll();
      setCampaigns(data.campaigns || []);
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to fetch campaigns');
    } finally {
      setLoading(false);
    }
  };

  const handlePublish = async (campaignId) => {
    setActionLoading((prev) => ({ ...prev, [campaignId]: 'publishing' }));
    setActionMessages((prev) => ({ ...prev, [campaignId]: null }));

    try {
      const result = await campaignAPI.publish(campaignId);
      setActionMessages((prev) => ({
        ...prev,
        [campaignId]: {
          type: 'success',
          text: `Published! Google Campaign ID: ${result.google_campaign_id}`,
        },
      }));
      
      // Refresh the list
      await fetchCampaigns();
    } catch (err) {
      setActionMessages((prev) => ({
        ...prev,
        [campaignId]: {
          type: 'error',
          text: err.response?.data?.error || 'Failed to publish campaign',
        },
      }));
    } finally {
      setActionLoading((prev) => ({ ...prev, [campaignId]: null }));
    }
  };

  const handleDisable = async (campaignId) => {
    if (!confirm('Are you sure you want to disable this campaign in Google Ads?')) {
      return;
    }

    setActionLoading((prev) => ({ ...prev, [campaignId]: 'disabling' }));
    setActionMessages((prev) => ({ ...prev, [campaignId]: null }));

    try {
      await campaignAPI.disable(campaignId);
      setActionMessages((prev) => ({
        ...prev,
        [campaignId]: {
          type: 'success',
          text: 'Campaign disabled successfully',
        },
      }));
      
      // Refresh the list
      await fetchCampaigns();
    } catch (err) {
      setActionMessages((prev) => ({
        ...prev,
        [campaignId]: {
          type: 'error',
          text: err.response?.data?.error || 'Failed to disable campaign',
        },
      }));
    } finally {
      setActionLoading((prev) => ({ ...prev, [campaignId]: null }));
    }
  };

  const handleDelete = async (campaignId, campaignName) => {
    if (!confirm(`Are you sure you want to delete "${campaignName}"?`)) {
      return;
    }

    setActionLoading((prev) => ({ ...prev, [campaignId]: 'deleting' }));

    try {
      await campaignAPI.delete(campaignId);
      await fetchCampaigns();
    } catch (err) {
      setActionMessages((prev) => ({
        ...prev,
        [campaignId]: {
          type: 'error',
          text: err.response?.data?.error || 'Failed to delete campaign',
        },
      }));
    } finally {
      setActionLoading((prev) => ({ ...prev, [campaignId]: null }));
    }
  };

  const getStatusBadge = (status) => {
    const statusStyles = {
      DRAFT: { backgroundColor: '#ffa726', color: 'white' },
      PUBLISHED: { backgroundColor: '#66bb6a', color: 'white' },
      PAUSED: { backgroundColor: '#ef5350', color: 'white' },
    };

    return (
      <span
        style={{
          ...styles.badge,
          ...statusStyles[status],
        }}
      >
        {status}
      </span>
    );
  };

  const formatDate = (dateString) => {
    if (!dateString) return 'N/A';
    return new Date(dateString).toLocaleDateString();
  };

  const formatBudget = (micros) => {
    if (!micros) return 'N/A';
    return `$${(micros / 1000000).toFixed(2)}`;
  };

  if (loading) {
    return (
      <div style={styles.container}>
        <h2 style={styles.heading}>All Campaigns</h2>
        <div style={styles.loading}>Loading campaigns...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div style={styles.container}>
        <h2 style={styles.heading}>All Campaigns</h2>
        <div style={styles.errorAlert}>{error}</div>
        <button onClick={fetchCampaigns} style={styles.retryButton}>
          Retry
        </button>
      </div>
    );
  }

  if (campaigns.length === 0) {
    return (
      <div style={styles.container}>
        <h2 style={styles.heading}>All Campaigns</h2>
        <div style={styles.emptyState}>
          <p>No campaigns yet. Create your first campaign above!</p>
        </div>
      </div>
    );
  }

  return (
    <div style={styles.container}>
      <div style={styles.header}>
        <h2 style={styles.heading}>All Campaigns</h2>
        <button onClick={fetchCampaigns} style={styles.refreshButton}>
          🔄 Refresh
        </button>
      </div>

      <div style={styles.tableContainer}>
        <table style={styles.table}>
          <thead>
            <tr style={styles.tableHeader}>
              <th style={styles.th}>Name</th>
              <th style={styles.th}>Objective</th>
              <th style={styles.th}>Type</th>
              <th style={styles.th}>Budget</th>
              <th style={styles.th}>Dates</th>
              <th style={styles.th}>Status</th>
              <th style={styles.th}>Google ID</th>
              <th style={styles.th}>Actions</th>
            </tr>
          </thead>
          <tbody>
            {campaigns.map((campaign) => (
              <React.Fragment key={campaign.id}>
                <tr style={styles.tableRow}>
                  <td style={styles.td}>
                    <strong>{campaign.name}</strong>
                  </td>
                  <td style={styles.td}>{campaign.objective || 'N/A'}</td>
                  <td style={styles.td}>{campaign.campaign_type}</td>
                  <td style={styles.td}>{formatBudget(campaign.daily_budget)}</td>
                  <td style={styles.td}>
                    <div style={styles.dates}>
                      <div>Start: {formatDate(campaign.start_date)}</div>
                      <div>End: {formatDate(campaign.end_date)}</div>
                    </div>
                  </td>
                  <td style={styles.td}>{getStatusBadge(campaign.status)}</td>
                  <td style={styles.td}>
                    {campaign.google_campaign_id || (
                      <span style={styles.mutedText}>Not published</span>
                    )}
                  </td>
                  <td style={styles.td}>
                    <div style={styles.actionButtons}>
                      {campaign.status === 'DRAFT' && (
                        <button
                          onClick={() => handlePublish(campaign.id)}
                          disabled={actionLoading[campaign.id]}
                          style={{
                            ...styles.actionButton,
                            ...styles.publishButton,
                          }}
                        >
                          {actionLoading[campaign.id] === 'publishing'
                            ? 'Publishing...'
                            : '📤 Publish'}
                        </button>
                      )}

                      {campaign.status === 'PUBLISHED' && (
                        <button
                          onClick={() => handleDisable(campaign.id)}
                          disabled={actionLoading[campaign.id]}
                          style={{
                            ...styles.actionButton,
                            ...styles.disableButton,
                          }}
                        >
                          {actionLoading[campaign.id] === 'disabling'
                            ? 'Disabling...'
                            : '⏸️ Pause'}
                        </button>
                      )}

                      <button
                        onClick={() => handleDelete(campaign.id, campaign.name)}
                        disabled={actionLoading[campaign.id]}
                        style={{
                          ...styles.actionButton,
                          ...styles.deleteButton,
                        }}
                      >
                        {actionLoading[campaign.id] === 'deleting'
                          ? 'Deleting...'
                          : '🗑️ Delete'}
                      </button>
                    </div>
                  </td>
                </tr>

                {actionMessages[campaign.id] && (
                  <tr>
                    <td colSpan="8" style={styles.td}>
                      <div
                        style={{
                          ...styles.messageBox,
                          ...(actionMessages[campaign.id].type === 'success'
                            ? styles.successMessage
                            : styles.errorMessage),
                        }}
                      >
                        {actionMessages[campaign.id].text}
                      </div>
                    </td>
                  </tr>
                )}
              </React.Fragment>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

const styles = {
  container: {
    backgroundColor: 'white',
    borderRadius: '8px',
    padding: '2rem',
    boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
  },
  header: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: '1.5rem',
  },
  heading: {
    margin: 0,
    fontSize: '1.5rem',
    color: '#333',
  },
  refreshButton: {
    padding: '0.5rem 1rem',
    border: '1px solid #ddd',
    borderRadius: '4px',
    backgroundColor: 'white',
    cursor: 'pointer',
    fontSize: '0.875rem',
  },
  loading: {
    textAlign: 'center',
    padding: '2rem',
    color: '#666',
  },
  errorAlert: {
    padding: '1rem',
    backgroundColor: '#ffebee',
    border: '1px solid #ef5350',
    borderRadius: '4px',
    color: '#c62828',
    marginBottom: '1rem',
  },
  retryButton: {
    padding: '0.75rem 1.5rem',
    backgroundColor: '#1a73e8',
    color: 'white',
    border: 'none',
    borderRadius: '4px',
    cursor: 'pointer',
  },
  emptyState: {
    textAlign: 'center',
    padding: '3rem',
    color: '#666',
  },
  tableContainer: {
    overflowX: 'auto',
  },
  table: {
    width: '100%',
    borderCollapse: 'collapse',
  },
  tableHeader: {
    backgroundColor: '#f5f5f5',
  },
  th: {
    padding: '1rem',
    textAlign: 'left',
    fontSize: '0.875rem',
    fontWeight: '600',
    color: '#333',
    borderBottom: '2px solid #e0e0e0',
  },
  tableRow: {
    borderBottom: '1px solid #e0e0e0',
  },
  td: {
    padding: '1rem',
    fontSize: '0.875rem',
    color: '#333',
  },
  dates: {
    fontSize: '0.75rem',
    color: '#666',
  },
  badge: {
    padding: '0.25rem 0.75rem',
    borderRadius: '12px',
    fontSize: '0.75rem',
    fontWeight: '600',
    display: 'inline-block',
  },
  mutedText: {
    color: '#999',
    fontStyle: 'italic',
  },
  actionButtons: {
    display: 'flex',
    gap: '0.5rem',
    flexWrap: 'wrap',
  },
  actionButton: {
    padding: '0.5rem 0.75rem',
    border: 'none',
    borderRadius: '4px',
    fontSize: '0.75rem',
    cursor: 'pointer',
    fontWeight: '500',
    whiteSpace: 'nowrap',
  },
  publishButton: {
    backgroundColor: '#1a73e8',
    color: 'white',
  },
  disableButton: {
    backgroundColor: '#ffa726',
    color: 'white',
  },
  deleteButton: {
    backgroundColor: '#ef5350',
    color: 'white',
  },
  messageBox: {
    padding: '0.75rem',
    borderRadius: '4px',
    fontSize: '0.875rem',
  },
  successMessage: {
    backgroundColor: '#e8f5e9',
    color: '#2e7d32',
    border: '1px solid #66bb6a',
  },
  errorMessage: {
    backgroundColor: '#ffebee',
    color: '#c62828',
    border: '1px solid #ef5350',
  },
};

export default CampaignList;
