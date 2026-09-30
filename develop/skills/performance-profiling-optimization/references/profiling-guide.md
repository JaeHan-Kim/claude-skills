# Profiling Guide

Symptom table, tools, bottleneck patterns, and the cost framing template for performance-profiling-optimization.

## Symptom to Likely Cause

| Symptom | Likely Cause |
|---------|-------------|
| CPU 100%, low latency variance | Hot loop, serialization overhead, regex |
| High P99, low CPU | Lock contention, thread starvation, GC stop-the-world |
| Memory grows then crashes | Memory leak, unbounded cache, large result sets held in memory |
| IO wait high | Slow DB queries, missing index, full table scans |
| Network latency spikes | DNS resolution, connection setup overhead, chatty API calls |
| GC pause > 200ms | Large old-gen, too-frequent allocation, premature promotion |

## Profiling Tool Guide

### CPU Profiling
**Goal**: find where CPU cycles are spent — hot methods, tight loops.

- **async-profiler** (JVM): low-overhead sampling profiler. Produces flame graphs.
  ```bash
  ./asprof -d 30 -f /tmp/flamegraph.html <pid>
  ```
- **py-spy** (Python): sampling profiler, no code changes needed.
  ```bash
  py-spy record -o profile.svg --pid <pid>
  ```
- **perf + FlameGraph** (Linux system-level):
  ```bash
  perf record -F 99 -p <pid> -g -- sleep 30
  perf script | stackcollapse-perf.pl | flamegraph.pl > cpu.svg
  ```
- **Reading a flame graph**: wide boxes = time-consuming. Look for wide plateaus near the top.

**Common CPU findings**: serialization/deserialization in hot path, regex compilation inside loops, reflection overhead, N+1 computation.

### Memory Profiling
**Goal**: find what's allocated, what's retained, and why GC can't collect it.

- **JVM heap dump**:
  ```bash
  jcmd <pid> GC.heap_dump /tmp/heap.hprof
  # Analyze with Eclipse MAT or VisualVM
  ```
- **GC log analysis** (JVM): enable with `-Xlog:gc*:file=/tmp/gc.log:time,uptime`
  - Look for: frequency of full GC, pause duration, heap occupancy after GC
  - Tool: GCEasy.io for visual analysis
- **Python memory**: `tracemalloc`, `memory_profiler`
- **Go**: `pprof` heap profile: `go tool pprof http://localhost:6060/debug/pprof/heap`

**Common memory findings**: static collections that grow unboundedly, event listeners never removed, large byte arrays for batch processing, connection/stream objects not closed.

### IO Profiling
**Goal**: find slow queries, missing indexes, excessive disk reads.

- **Slow query log** (MySQL/PostgreSQL):
  ```sql
  -- PostgreSQL
  SET log_min_duration_statement = 100; -- log queries > 100ms
  SELECT * FROM pg_stat_statements ORDER BY total_time DESC LIMIT 20;
  ```
- **EXPLAIN ANALYZE**: run on any query taking > 50ms.
- **strace** (Linux): trace syscalls for a process.
  ```bash
  strace -p <pid> -e trace=read,write,open,close -T 2>&1 | head -100
  ```
- **iotop**: identify processes doing most IO.

### Network Profiling
**Goal**: find latency between services, connection overhead, chattiness.

- **Distributed tracing** (Jaeger, Zipkin, OpenTelemetry): span timings across services.
- **tcpdump / Wireshark**: packet-level inspection.
- **curl with timing**:
  ```bash
  curl -w "@curl-format.txt" -o /dev/null -s https://api.example.com/endpoint
  # Shows: dns, connect, tls, TTFB, total
  ```
- **Connection reuse**: check if HTTP keep-alive is enabled; check connection pool hit rate.


## Common Bottleneck Patterns

### N+1 Query
**Signature**: DB query count scales linearly with result set size. Latency low per query, high in aggregate.
**Fix**: batch load with `IN (...)`, use JOIN, or add a data loader.

### Thread Pool Exhaustion
**Signature**: requests queue up, latency spikes, thread count at max, CPU low.
**Fix**: increase pool size (carefully), or reduce work per thread, or use async I/O.

### Memory Leak → GC Pressure → Latency Spikes
**Signature**: heap grows over hours/days, full GC frequency increases, P99 spikes correlate with GC events.
**Fix**: find the retention root via heap dump; fix the leak; tune GC only as a temporary measure.

### Hot Lock / Synchronized Block
**Signature**: high CPU, many threads in BLOCKED state in thread dump.
**Fix**: reduce lock scope, use lock-free data structures, partition the lock.

### Large Serialization Payload
**Signature**: high CPU on serialization threads, large response sizes, high memory allocation rate.
**Fix**: project only needed fields, paginate, use binary formats (protobuf, avro) for internal APIs.


## Making the Case for Performance Work

Frame performance work in cost and user impact terms — not engineering elegance.

**Template**:
> "Current P99 latency is X ms. Industry benchmark / SLA target is Y ms.
> At our traffic of Z RPS, each 100ms of extra latency costs approximately [conversion rate / user satisfaction / infra cost].
> Proposed fix requires [N days]. Expected outcome: P99 drops to W ms, [cost/impact metric] improves by K%."



**Stack coverage note:** Tool examples in this skill are JVM (async-profiler, heap dumps, GC logs), Python (py-spy, memory-profiler), and Go (pprof) centric. For Node.js: use `clinic.js` or `--inspect` with Chrome DevTools. For Rust: use `cargo flamegraph` or `perf`. The investigation workflow (measure → hypothesize → profile → fix → verify) applies to all stacks regardless of tooling.
