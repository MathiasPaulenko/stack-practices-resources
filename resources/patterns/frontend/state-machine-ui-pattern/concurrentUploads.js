// concurrentUploads.js — multiple file uploads as actors
import { createMachine, spawn, assign } from 'xstate';
import uploadMachine from './fileUploadMachine';

const batchUploadMachine = createMachine({
  id: 'batchUpload',
  initial: 'idle',
  context: { uploads: [] },
  states: {
    idle: {
      on: {
        ADD_FILES: {
          actions: assign({
            uploads: (ctx, event) =>
              event.files.map(file => ({
                file,
                ref: spawn(uploadMachine.withContext({ file })),
              })),
          }),
        },
      },
    },
  },
});
