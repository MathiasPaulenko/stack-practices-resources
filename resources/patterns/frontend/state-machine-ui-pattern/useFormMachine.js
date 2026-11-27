// useFormMachine.js — simple FSM with useReducer
import { useReducer, useCallback } from 'react';

const states = {
  IDLE: 'idle',
  SUBMITTING: 'submitting',
  SUCCESS: 'success',
  ERROR: 'error',
};

const initialState = { state: states.IDLE, data: null, error: null };

function formReducer(state, action) {
  switch (state.state) {
    case states.IDLE:
      if (action.type === 'SUBMIT') {
        return { state: states.SUBMITTING, data: null, error: null };
      }
      return state;

    case states.SUBMITTING:
      if (action.type === 'SUCCESS') {
        return { state: states.SUCCESS, data: action.data, error: null };
      }
      if (action.type === 'ERROR') {
        return { state: states.ERROR, data: null, error: action.error };
      }
      return state;

    case states.SUCCESS:
      if (action.type === 'RESET') {
        return initialState;
      }
      return state;

    case states.ERROR:
      if (action.type === 'RETRY') {
        return { state: states.SUBMITTING, data: null, error: null };
      }
      if (action.type === 'RESET') {
        return initialState;
      }
      return state;

    default:
      return state;
  }
}

function useFormMachine(submitFn) {
  const [state, dispatch] = useReducer(formReducer, initialState);

  const submit = useCallback(async (formData) => {
    dispatch({ type: 'SUBMIT' });
    try {
      const data = await submitFn(formData);
      dispatch({ type: 'SUCCESS', data });
    } catch (error) {
      dispatch({ type: 'ERROR', error: error.message });
    }
  }, [submitFn]);

  const retry = useCallback(() => dispatch({ type: 'RETRY' }), []);
  const reset = useCallback(() => dispatch({ type: 'RESET' }), []);

  return { ...state, submit, retry, reset };
}

export { states, useFormMachine };
