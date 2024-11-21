# Testing Strategy Planning

## Possible Testing Strategies

All testing strategies learnt in class are listed below.
Testing strategies which are not possible for our chosen application are crossed out.
Only testing strategies which we have selected to perform are checked.

## Black Box

- [ ] Random testing
- [ ] Failure/dirty tests / error guessing
- [ ] Checklists
- [ ] ~~Operational profiles~~
- [ ] Input domain testing
  - [ ] Equivalence classes / partitioning
    - [ ] Weak normal equivalence class testing
    - [ ] Strong normal equivalence class testing
  - [ ] Boundary value analysis
    - [ ] Extreme point combination
    - [ ] N x 1
      - [ ] Weak N x 1
      - [ ] Strong N x 1
- [ ] Decision tables
- [ ] Cause-effect graphs
- [ ] ~~Syntax-driven testing~~
- [ ] Finite state machines (coverage)
  - [ ] Unified Markov model (usage based testing)
- [ ] Combinatorial testing
  - [ ] Pairwise testing
  - [ ] Functional testing (input-output analysis)

## White Box

- [ ] Control flow coverage
  - [ ] Control flow graph
  - [ ] Statement coverage
  - [ ] Branch coverage
  - [ ] Condition/predicate coverage
  - [ ] Modified condition/predicate coverage
  - [ ] Path coverage
  - [ ] Symbolic execution
  - [ ] Concolic testing
    - [ ] Reverse path analysis
- [ ] Data flow coverage
  - [ ] Static data flow testing
    - [ ] Data definition, use and dependency analysis
      - [ ] All p-use some c-use testing
      - [ ] All c-use some p-use testing
      - [ ] All-use testing
  - [ ] Dynamic data flow testing
    - [ ] Data dependency graphs
      - [ ] Data slices
- [ ] Error flow coverage
  - [ ] ~~Statistical testing~~
    - [ ] ~~Fault seeding~~
    - [ ] ~~Independent tests~~
  - [ ] Software mutations
    - [ ] Value mutations
    - [ ] Decision mutations
    - [ ] Statement mutations
    - [ ] Mothra

## Integration

- [ ] Dependency graphs
- [ ] Call graphs
- [ ] Paths
- [ ] Non-incremental testing (big bang)
- [ ] Incremental testing
  - [ ] Bottom-up
  - [ ] Top-down
  - [ ] Sandwich testing
  - [ ] Modified sandwich testing
- [ ] Collaboration integration
- [ ] Layer integration
