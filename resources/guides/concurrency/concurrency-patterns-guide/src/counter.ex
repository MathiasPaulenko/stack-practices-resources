# Actor model on the BEAM VM: each GenServer owns its state exclusively
# and talks to the world through messages in its mailbox.
# Run: elixir counter.ex

defmodule Counter do
  use GenServer

  def start_link(initial_value \\ 0) do
    GenServer.start_link(__MODULE__, initial_value)
  end

  def increment(pid), do: GenServer.call(pid, :increment)
  def get_value(pid), do: GenServer.call(pid, :get_value)

  @impl true
  def init(initial_value), do: {:ok, initial_value}

  @impl true
  def handle_call(:increment, _from, state) do
    new_state = state + 1
    {:reply, new_state, new_state}
  end

  def handle_call(:get_value, _from, state) do
    {:reply, state, state}
  end
end

{:ok, counter1} = Counter.start_link(0)
{:ok, counter2} = Counter.start_link(100)

IO.inspect(Counter.increment(counter1), label: "counter1 +1")
IO.inspect(Counter.increment(counter1), label: "counter1 +1")
IO.inspect(Counter.get_value(counter2), label: "counter2 (isolated)")
