<script>
  import { counter } from "./stores/counter.js";
  import { currentTime } from "./stores/time.js";
</script>

<h1>Count: {$counter}</h1>
<button on:click={counter.increment}>+</button>
<button on:click={counter.decrement}>-</button>
<button on:click={counter.reset}>Reset</button>

<p>Current time: {$currentTime.toLocaleTimeString()}</p>
