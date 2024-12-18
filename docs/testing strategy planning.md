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
- [x] Input domain testing (Katharine)
  - [x] Equivalence classes / partitioning (Katharine)
    - [x] Weak normal equivalence class testing (Katharine)
    - [ ] Strong normal equivalence class testing
  - [x] Boundary value analysis (Yenosibina)
    - [x] Extreme point combination (Yenosibina)
    - [x] N x 1 (Yenosibina)
      - [x] Weak N x 1 (Yenosibina)
      - [x] Strong N x 1 (Yenosibina)
- [x] Decision tables
- [x] Cause-effect graphs
- [ ] ~~Syntax-driven testing~~
- [x] Finite state machines (coverage)
  - [ ] ~~Unified Markov model (usage based testing)~~
- [x] Combinatorial testing (Yenosibina)
  - [x] Pairwise testing (Yenosibina)
  - [x] Functional testing (input-output analysis) (Yenosibina)

## White Box

- [x] Control flow coverage (Abdulaziz)
  - [x] Control flow graph (Abdulaziz)
  - [x] Statement coverage (Abdulaziz)
  - [x] Branch coverage (Abdulaziz)
  - [ ] Condition/predicate coverage
  - [ ] Modified condition/predicate coverage
  - [ ] Path coverage
  - [ ] Symbolic execution
  - [ ] Concolic testing
    - [ ] Reverse path analysis
- [x] Data flow coverage (Cedric)
  - [x] Static data flow testing (Cedric)
    - [x] Data definition, use and dependency analysis (Cedric)
      - [x] All p-use some c-use testing (Cedric)
      - [x] All c-use some p-use testing (Cedric)
      - [x] All-use testing (Cedric)
  - [x] Dynamic data flow testing
    - [x] Data dependency graphs
      - [x] Data slices
- [x] Error flow coverage
  - [ ] ~~Statistical testing~~
    - [ ] ~~Fault seeding~~
    - [ ] ~~Independent tests~~
  - [x] Software mutations (James)
    - [x] Value mutations (James)
    - [x] Decision mutations (James)
    - [x] Statement mutations (James)
    - [x] Mothra (James)

### Integration

- [x] Dependency graphs (Jeremy)
- [x] Call graphs (Jeremy)
- [ ] ~~Paths (Yenosibina)~~
- [x] Non-incremental testing (big bang) (Yenosibina & Aziz)
- [x] Incremental testing (Jeremy)
  - [x] Bottom-up (Jeremy)
  - [ ] Top-down
  - [ ] Sandwich testing
  - [ ] Modified sandwich testing
- [ ] Collaboration integration
- [ ] Layer integration
