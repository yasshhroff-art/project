/**
 * CampaignForm component
 * Form for creating and editing campaigns with validation
 */

import React, { useState } from 'react';
import { useForm } from 'react-hook-form';
import { campaignAPI } from '../services/api';

const CampaignForm = ({ onSuccess }) => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);

  const {
    register,
    handleSubmit,
    formState: { errors },
    reset,
  } = useForm({
    defaultValues: {
      name: '',
      objective: 'SALES',
      campaign_type: 'DEMAND_GEN',
      daily_budget: 50000,
      start_date: '',
      end_date: '',
      ad_group_name: 'Main Ad Group',
      ad_headline: '',
      ad_description: '',
      asset_url: '',
    },
  });

  const onSubmit = async (data) => {
    setLoading(true);
    setError(null);
    setSuccess(null);

    try {
      const result = await campaignAPI.create(data);
      setSuccess('Campaign created successfully!');
      reset();
      if (onSuccess) {
        onSuccess(result.campaign);
      }
      
      // Clear success message after 3 seconds
      setTimeout(() => setSuccess(null), 3000);
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to create campaign');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={styles.container}>
      <h2 style={styles.heading}>Create New Campaign</h2>

      {error && (
        <div style={styles.errorAlert}>
          <strong>Error:</strong> {error}
        </div>
      )}

      {success && (
        <div style={styles.successAlert}>
          <strong>Success:</strong> {success}
        </div>
      )}

      <form onSubmit={handleSubmit(onSubmit)} style={styles.form}>
        <div style={styles.row}>
          <div style={styles.formGroup}>
            <label style={styles.label}>
              Campaign Name <span style={styles.required}>*</span>
            </label>
            <input
              type="text"
              {...register('name', { required: 'Campaign name is required' })}
              style={styles.input}
              placeholder="e.g., Summer Sale 2024"
            />
            {errors.name && (
              <span style={styles.errorText}>{errors.name.message}</span>
            )}
          </div>

          <div style={styles.formGroup}>
            <label style={styles.label}>Objective</label>
            <select {...register('objective')} style={styles.select}>
              <option value="SALES">Sales</option>
              <option value="LEADS">Leads</option>
              <option value="WEBSITE_TRAFFIC">Website Traffic</option>
              <option value="BRAND_AWARENESS">Brand Awareness</option>
              <option value="APP_PROMOTION">App Promotion</option>
            </select>
          </div>
        </div>

        <div style={styles.row}>
          <div style={styles.formGroup}>
            <label style={styles.label}>Campaign Type</label>
            <input
              type="text"
              {...register('campaign_type')}
              style={styles.input}
              placeholder="DEMAND_GEN"
            />
          </div>

          <div style={styles.formGroup}>
            <label style={styles.label}>
              Daily Budget (micros)
              <span style={styles.helpText}> $1 = 1,000,000 micros</span>
            </label>
            <input
              type="number"
              {...register('daily_budget', {
                min: { value: 0, message: 'Budget must be positive' },
              })}
              style={styles.input}
              placeholder="50000"
            />
            {errors.daily_budget && (
              <span style={styles.errorText}>{errors.daily_budget.message}</span>
            )}
          </div>
        </div>

        <div style={styles.row}>
          <div style={styles.formGroup}>
            <label style={styles.label}>Start Date</label>
            <input
              type="date"
              {...register('start_date')}
              style={styles.input}
            />
          </div>

          <div style={styles.formGroup}>
            <label style={styles.label}>End Date</label>
            <input
              type="date"
              {...register('end_date')}
              style={styles.input}
            />
          </div>
        </div>

        <div style={styles.formGroup}>
          <label style={styles.label}>Ad Group Name</label>
          <input
            type="text"
            {...register('ad_group_name')}
            style={styles.input}
            placeholder="Main Ad Group"
          />
        </div>

        <div style={styles.formGroup}>
          <label style={styles.label}>
            Ad Headline <span style={styles.required}>*</span>
          </label>
          <input
            type="text"
            {...register('ad_headline', {
              required: 'Ad headline is required',
              maxLength: { value: 30, message: 'Maximum 30 characters' },
            })}
            style={styles.input}
            placeholder="Amazing Summer Deals!"
            maxLength={30}
          />
          {errors.ad_headline && (
            <span style={styles.errorText}>{errors.ad_headline.message}</span>
          )}
        </div>

        <div style={styles.formGroup}>
          <label style={styles.label}>Ad Description</label>
          <textarea
            {...register('ad_description')}
            style={styles.textarea}
            placeholder="Save up to 50% on all products. Limited time offer!"
            rows={3}
          />
        </div>

        <div style={styles.formGroup}>
          <label style={styles.label}>Asset URL (Final URL)</label>
          <input
            type="url"
            {...register('asset_url')}
            style={styles.input}
            placeholder="https://example.com/summer-sale"
          />
        </div>

        <div style={styles.buttonGroup}>
          <button
            type="submit"
            disabled={loading}
            style={{
              ...styles.button,
              ...styles.primaryButton,
              ...(loading ? styles.buttonDisabled : {}),
            }}
          >
            {loading ? 'Creating...' : 'Save Campaign Locally'}
          </button>

          <button
            type="button"
            onClick={() => reset()}
            style={{ ...styles.button, ...styles.secondaryButton }}
            disabled={loading}
          >
            Clear Form
          </button>
        </div>
      </form>
    </div>
  );
};

const styles = {
  container: {
    backgroundColor: 'white',
    borderRadius: '8px',
    padding: '2rem',
    boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
    marginBottom: '2rem',
  },
  heading: {
    margin: '0 0 1.5rem 0',
    fontSize: '1.5rem',
    color: '#333',
  },
  form: {
    display: 'flex',
    flexDirection: 'column',
    gap: '1rem',
  },
  row: {
    display: 'grid',
    gridTemplateColumns: '1fr 1fr',
    gap: '1rem',
  },
  formGroup: {
    display: 'flex',
    flexDirection: 'column',
    gap: '0.5rem',
  },
  label: {
    fontSize: '0.875rem',
    fontWeight: '500',
    color: '#333',
  },
  required: {
    color: '#d32f2f',
  },
  helpText: {
    fontSize: '0.75rem',
    color: '#666',
    fontWeight: 'normal',
  },
  input: {
    padding: '0.75rem',
    border: '1px solid #ddd',
    borderRadius: '4px',
    fontSize: '1rem',
    transition: 'border-color 0.2s',
  },
  select: {
    padding: '0.75rem',
    border: '1px solid #ddd',
    borderRadius: '4px',
    fontSize: '1rem',
    backgroundColor: 'white',
    cursor: 'pointer',
  },
  textarea: {
    padding: '0.75rem',
    border: '1px solid #ddd',
    borderRadius: '4px',
    fontSize: '1rem',
    fontFamily: 'inherit',
    resize: 'vertical',
  },
  buttonGroup: {
    display: 'flex',
    gap: '1rem',
    marginTop: '1rem',
  },
  button: {
    padding: '0.75rem 1.5rem',
    border: 'none',
    borderRadius: '4px',
    fontSize: '1rem',
    fontWeight: '500',
    cursor: 'pointer',
    transition: 'all 0.2s',
  },
  primaryButton: {
    backgroundColor: '#1a73e8',
    color: 'white',
  },
  secondaryButton: {
    backgroundColor: '#f5f5f5',
    color: '#333',
  },
  buttonDisabled: {
    opacity: 0.6,
    cursor: 'not-allowed',
  },
  errorAlert: {
    padding: '1rem',
    backgroundColor: '#ffebee',
    border: '1px solid #ef5350',
    borderRadius: '4px',
    color: '#c62828',
    marginBottom: '1rem',
  },
  successAlert: {
    padding: '1rem',
    backgroundColor: '#e8f5e9',
    border: '1px solid #66bb6a',
    borderRadius: '4px',
    color: '#2e7d32',
    marginBottom: '1rem',
  },
  errorText: {
    fontSize: '0.75rem',
    color: '#d32f2f',
  },
};

export default CampaignForm;
