// fileUploadMachine.js — nested states
import { createMachine, assign } from 'xstate';

const uploadMachine = createMachine({
  id: 'upload',
  initial: 'idle',
  context: { progress: 0, file: null, url: null },
  states: {
    idle: {
      on: { SELECT_FILE: { target: 'selected', actions: assign({ file: (_, e) => e.file }) } },
    },
    selected: {
      on: { START: 'uploading', CANCEL: 'idle' },
    },
    uploading: {
      initial: 'sending',
      states: {
        sending: {
          on: {
            PROGRESS: { actions: assign({ progress: (_, e) => e.progress }) },
            COMPLETE: { target: 'done', actions: assign({ url: (_, e) => e.url }) },
            FAIL: 'failed',
          },
        },
        failed: {
          on: { RETRY: 'sending' },
        },
        done: { type: 'final' },
      },
      on: { CANCEL: 'idle' },
    },
  },
});
