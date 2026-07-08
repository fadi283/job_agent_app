import React, { useEffect } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { setJobs } from '../store/jobsSlice';
import axios from 'axios';
import { Briefcase } from 'lucide-react';

const Dashboard = () => {
  const dispatch = useDispatch();
  const { items: jobs, status } = useSelector((state) => state.jobs);

  useEffect(() => {
    // Placeholder API call to fetch jobs
    const fetchJobs = async () => {
      try {
        const response = await axios.get('http://localhost:8000/api/v1/jobs/');
        dispatch(setJobs(response.data));
      } catch (error) {
        console.error('Error fetching jobs:', error);
      }
    };
    
    fetchJobs();
  }, [dispatch]);

  return (
    <div className="animate-fade-in" style={{ paddingTop: '2rem' }}>
      <h1>Dashboard</h1>
      <p>Manage your job applications and generated resumes.</p>
      
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))', gap: '1.5rem', marginTop: '2rem' }}>
        {jobs.length === 0 ? (
          <div className="glass-panel" style={{ padding: '2rem', textAlign: 'center', gridColumn: '1 / -1' }}>
            <Briefcase size={48} style={{ color: 'var(--text-tertiary)', margin: '0 auto 1rem auto' }} />
            <h3>No jobs found</h3>
            <p>You haven't tracked any jobs yet. Start by creating one via the backend API!</p>
          </div>
        ) : (
          jobs.map(job => (
            <div key={job.id} className="glass-panel" style={{ padding: '1.5rem' }}>
              <h3>{job.title}</h3>
              <p style={{ color: 'var(--accent-primary)', fontWeight: 500 }}>{job.company}</p>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginTop: '1rem' }}>
                <span style={{ 
                  background: 'var(--bg-tertiary)', 
                  padding: '0.25rem 0.5rem', 
                  borderRadius: 'var(--radius-sm)',
                  fontSize: '0.875rem'
                }}>
                  {job.status}
                </span>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
};

export default Dashboard;
