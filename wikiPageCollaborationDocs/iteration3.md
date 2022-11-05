# Requirements Analysis Document (RAD)

### 1. Introduction

i. Purpose of the System

ii. Scope of the system

iii. Objectives and success criteria of the project

iv. Definitions, acronyms, and abbreviations

v. References

vi. Overview

***
### 2. Current System

***
3. ### Proposed System

   - #### Overview:

     We will pull down Tweets from the specified companies, store them in a database. We will then use VADER analysis to rate the Tweets according to the scores previously requested by Donaldson Company (Positive/Neutral/Negative/Compound) and store those values alongside the Tweets in question.

     In addition to this tone analysis, we will also attempt to flag any tweet that may potentially be about a particular alternative powertrain, for any analysis that might be done on it.

     In addition to this, we will attempt to build methods of extracting potentially useful information from the Tweets gathered, such as frequency mentioning various powertrains, how frequently those mentions occur in the context of how frequently the company tweets overall, whether the frequency is changing, etc.

   - Functional requirements