import { createSlice } from '@reduxjs/toolkit';

const initialState = {
  items: [],
  status: 'idle', // 'idle' | 'loading' | 'succeeded' | 'failed'
  error: null,
};

const jobsSlice = createSlice({
  name: 'jobs',
  initialState,
  reducers: {
    setJobs: (state, action) => {
      state.items = action.payload;
    },
    addJob: (state, action) => {
      state.items.push(action.payload);
    },
  },
});

export const { setJobs, addJob } = jobsSlice.actions;
export default jobsSlice.reducer;
