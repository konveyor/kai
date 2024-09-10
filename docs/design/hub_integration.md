# Engineering Approach for Kai Integration into Konveyor

## Objective

To integrate the AI component Kai into Konveyor, focusing on stored analysis and solved incident component work.

## Overview

Kai will be integrated as a bolt-on service with its own dedicated database, monitoring and interacting with Konveyor via the Hub API. The integration involves several key components:

1. **Konveyor Hub API**
1. **Hub Importer Service**
1. **Kai Service**
1. **Dedicated Kai Database**
1. **Analysis and Diff Generation**
1. **Konveyor Operator**

## Component Descriptions

### Konveyor Hub API

The Konveyor Hub API operates independently, generating and updating analysis reports that will be processed by Kai.

### Hub Importer Service

The Hub Importer Service polls the Konveyor Hub API for new or updated analysis reports. It retrieves data from the Konveyor Hub API and directly processes and stores it in the shared database with Kai for use in prompting.

### Kai Service

The Kai Service acts as the main processing unit for Kai, handling the data stored in the shared database. It uses data from the shared database, managed by the Hub Importer Service, in order to generate higher quality prompts.

### Analysis and Diff Generation

The Analysis and Diff Generation component processes incoming analysis reports to identify changes and resolved incidents. It compares new reports with previous ones to generate diffs, which highlight these changes.

### Dedicated Kai Database

The Dedicated Kai Database stores all the analysis reports, diffs, and related data for Kai. It provides a long-term storage solution to support future analyses and recomputations.

### Konveyor Operator

The Konveyor Operator will facilitate the deployment and management of Konveyor and Kai.

## Data Flow

1. The **Konveyor Hub API** operates independently, generating and updating analysis reports through normal use.
1. The **Hub Importer Service** polls the Konveyor Hub API for new or updated reports.
1. The importer processes the analysis reports and stores it directly in the **Dedicated Kai Database**, shared with the Kai Service.
1. The **Kai Service** retrieves the data stored in the shared database when building RAG prompts to send to LLMs.

## Usage and Improvement

- **Incident Mining:** As Kai ingests more reports and finds solutions, these solved incidents are used to improve the RAG (Retrieval-Augmented Generation) prompts that Kai sends to the LLMs (Large Language Models).
- **Continuous Improvement:** The system continuously learns from the ingested data, enhancing its ability to generate accurate and useful insights over time.

This architecture ensures a seamless integration of Kai into Konveyor, providing robust data processing and storage capabilities to enhance the overall functionality of the system.
