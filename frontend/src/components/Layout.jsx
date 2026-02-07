/**
 * Layout component
 * Provides consistent header and container for all pages
 */

import React from 'react';

const Layout = ({ children }) => {
  return (
    <div style={styles.container}>
      <header style={styles.header}>
        <div style={styles.headerContent}>
          <h1 style={styles.title}>Google Ads Campaign Manager</h1>
          <p style={styles.subtitle}>Create and publish marketing campaigns</p>
        </div>
      </header>
      
      <main style={styles.main}>
        {children}
      </main>
      
      <footer style={styles.footer}>
        <p style={styles.footerText}>
          Built with React + Flask + PostgreSQL + Google Ads API
        </p>
      </footer>
    </div>
  );
};

const styles = {
  container: {
    minHeight: '100vh',
    display: 'flex',
    flexDirection: 'column',
    backgroundColor: '#f5f5f5',
  },
  header: {
    backgroundColor: '#1a73e8',
    color: 'white',
    padding: '2rem 1rem',
    boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
  },
  headerContent: {
    maxWidth: '1200px',
    margin: '0 auto',
  },
  title: {
    margin: 0,
    fontSize: '2rem',
    fontWeight: 'bold',
  },
  subtitle: {
    margin: '0.5rem 0 0 0',
    fontSize: '1rem',
    opacity: 0.9,
  },
  main: {
    flex: 1,
    maxWidth: '1200px',
    width: '100%',
    margin: '0 auto',
    padding: '2rem 1rem',
  },
  footer: {
    backgroundColor: '#fff',
    borderTop: '1px solid #e0e0e0',
    padding: '1rem',
    textAlign: 'center',
  },
  footerText: {
    margin: 0,
    color: '#666',
    fontSize: '0.875rem',
  },
};

export default Layout;
