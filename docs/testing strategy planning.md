# Testing Strategy Planning

## Possible Testing Strategies

All testing strategies learnt in class are listed below.
Testing strategies which are not possible for our chosen application are crossed out.
Only testing strategies which we have selected to perform are checked.

## Black Box

- [ ] Random testing
- [x] Failure/dirty tests / error guessing
- [ ] Checklists
- [ ] ~~Operational profiles~~
- [x] Input domain testing
  - [x] Equivalence classes / partitioning
    - [x] Weak normal equivalence class testing
    - [ ] Strong normal equivalence class testing
  - [ ] Boundary value analysis
    - [ ] Extreme point combination
    - [ ] N x 1
      - [ ] Weak N x 1
      - [ ] Strong N x 1
- [x] Decision tables
- [x] Cause-effect graphs
- [ ] ~~Syntax-driven testing~~
- [x] Finite state machines (coverage)
  - [ ] ~~Unified Markov model (usage based testing)~~
- [x] Combinatorial testing
  - [x] Pairwise testing
  - [ ] Functional testing (input-output analysis)

## White Box

- [x] Control flow coverage
  - [x] Control flow graph
  - [x] Statement coverage
  - [x] Branch coverage
  - [ ] Condition/predicate coverage
  - [ ] Modified condition/predicate coverage
  - [ ] Path coverage
  - [ ] Symbolic execution
  - [ ] Concolic testing
    - [ ] Reverse path analysis
- [x] Data flow coverage
  - [x] Static data flow testing
    - [x] Data definition, use and dependency analysis
      - [x] All p-use some c-use testing
      - [x] All c-use some p-use testing
      - [x] All-use testing
  - [x] Dynamic data flow testing
    - [x] Data dependency graphs
      - [x] Data slices
- [x] Error flow coverage
  - [ ] ~~Statistical testing~~
    - [ ] ~~Fault seeding~~
    - [ ] ~~Independent tests~~
  - [x] Software mutations
    - [x] Value mutations
    - [x] Decision mutations
    - [x] Statement mutations
    - [x] Mothra

### Integration

- [x] Dependency graphs
- [x] Call graphs
- [ ] Paths
- [ ] Non-incremental testing (big bang)
- [x] Incremental testing
  - [x] Bottom-up
  - [ ] Top-down
  - [ ] Sandwich testing
  - [ ] Modified sandwich testing
- [ ] Collaboration integration
- [ ] Layer integration
