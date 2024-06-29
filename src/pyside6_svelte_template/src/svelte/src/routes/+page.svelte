<script>
    import { onMount } from 'svelte';

    $:count = 0;
    let timeStamp = (new Date()).toISOString();

    function increaseCount() {
        count += 1;
        window.bridge.show_count(count);
    }

    function decreaseCount() {
        if (count > 0) {
            count -= 1;
            window.bridge.show_count(count);
        }
    }

    onMount(() => {
        window.bridge.show_timestamp.connect(newTimeStamp => {
            timeStamp = newTimeStamp;
        });
    });
</script>

<style>
    .container {
        text-align: center;
        padding: 20px;
    }
    .countButton {
        margin: 5px;
    }
</style>

<div class="container">
    <h1>Counter: {count}</h1>
    <button class="countButton" on:click={increaseCount}>Increase</button>
    <button class="countButton" on:click={decreaseCount}>Decrease</button>
    <h2>Current Time: {timeStamp}</h2>
</div>
