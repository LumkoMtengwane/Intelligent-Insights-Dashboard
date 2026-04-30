# Data Analysis & Insights Dashboard

This is a powerful Streamlit application for automated data analysis, quality assessment, and AI-powered insights. As a data professional, I understand that adequate data preprocessing is a big part of the data pipeline and that exploratory data analysis informs a big part of preprocessing decisions, therefore I created this dashboard that helps you understand your data through interactive visualizations, statistical summaries, and machine learning recommendations.

## Features

 **Core Features:**
-  **Data Upload & Exploration** - Upload CSV files and explore data interactively
-  **Data Profiling** - Automatic data type detection and statistical summaries
-  **Data Quality Checks** - Identify missing values, outliers, and data issues
-  **Interactive Visualizations** - Dynamic charts with Plotly (histograms, scatter plots, heatmaps, etc.)
-  **AI-Powered Insights** - Generate insights using Azure OpenAI
-  **ML Recommendations** - Automatic machine learning task detection and model suggestions
-  **Natural Language Queries** - Ask questions about your data in plain English
-  **Report Generation** - Export findings as PDF reports
-  **Cloud Storage Integration** - Upload charts and reports to Azure Blob Storage
-  **LLM Observability** - Track and trace all AI/LLM calls with Langfuse

## Quick Start

### Prerequisites
- Python 3.10+
- Git
- Azure OpenAI API access (for AI features)
- Optional: Azure Search, Azure Blob Storage, Langfuse account

### Installation

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd day9_streamlit
   ```

2. **Create a virtual environment:**
   ```bash
   # Windows
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   
   # macOS/Linux
   python -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   ```bash
   # Copy the example file
   cp .env.example .env
   
   # Edit .env with your Azure credentials
   # See .env.example for all required variables
   ```

5. **Run the app:**
   ```bash
   streamlit run app.py
   ```

   The app will open at: `http://localhost:8501`

## Configuration

### Required Azure Services

**1. Azure OpenAI (Required for AI features)**
- Deploy `gpt-4` or similar model for chat
- Deploy `text-embedding-3-small` or similar for embeddings
- Get API keys and endpoints from Azure Portal

**2. Azure AI Search (Optional - for semantic search)**
- Create an AI Search service
- Create an index for your data
- Add AZURE_SEARCH_* credentials to .env

**3. Azure Blob Storage (Optional - for storing reports)**
- Create a storage account and container
- Add connection string to .env

**4. Langfuse (Optional - for LLM observability)**
- Sign up at https://cloud.langfuse.com
- Add your API keys to .env

### Environment Variables

See `.env.example` for a complete list. At minimum, set:
```
AZURE_OPENAI_API_KEY
AZURE_OPENAI_ENDPOINT
AZURE_OPENAI_CHAT_DEPLOYMENT
AZURE_OPENAI_CHAT_API_VERSION
```

## Usage

1. **Upload Data** - Use the sidebar to upload a CSV file
2. **Explore** - View data summary, quality metrics, and statistics
3. **Visualize** - Generate interactive charts
4. **Generate Insights** - Use AI to get automatic data insights
5. **Get ML Recommendations** - Discover suitable ML tasks and models
6. **Ask Questions** - Query your data using natural language
7. **Export** - Download reports as PDF or upload to cloud storage

## Project Structure

```
day9_streamlit/
├── app.py                      # Main Streamlit application
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variables template
├── services/                  # Business logic modules
│   ├── data_loader.py
│   ├── data_quality.py
│   ├── data_profiler.py
│   ├── chart_builder.py
│   ├── chart_generator.py
│   ├── insights_engine.py     # AI-powered insights
│   ├── ml_recommender.py      # ML task detection
│   ├── query_engine.py        # Natural language queries
│   ├── blob_storage.py        # Azure Blob integration
│   ├── report_generator.py    # PDF export
│   └── langfuse_tracker.py    # LLM tracing
├── ui/                        # UI components
│   ├── layout.py
│   ├── sidebar.py
│   └── dashboard_components.py
└── utils/                     # Helper functions
    ├── helpers.py
    ├── validators.py
    └── chart_theme.py
```

## Technologies Used

- **Framework:** Streamlit
- **Data Processing:** Pandas, NumPy
- **Visualization:** Plotly
- **AI/LLM:** Azure OpenAI, Langfuse
- **Search:** Azure AI Search
- **Storage:** Azure Blob Storage
- **PDF Export:** ReportLab / PyPDF
- **Environment:** python-dotenv

## Troubleshooting

### "ModuleNotFoundError" when running app
```bash
# Reinstall dependencies
pip install -r requirements.txt
```

### Azure API errors
- Verify all .env variables are correct
- Check API key expiration in Azure Portal
- Ensure deployment names match your Azure resources

### Streamlit not connecting to Azure services
- Check your internet connection
- Verify firewall/network settings
- Test Azure credentials with: `python -c "from openai import AzureOpenAI; print('✓ Connected')"`

## Development

To extend the app:
1. Add new analysis functions in `services/`
2. Create UI components in `ui/`
3. Update requirements.txt with new dependencies
4. Test locally before pushing

## Performance Tips

- Smaller datasets load faster
- Use data filtering for large files
- Cache results for repeated queries
- Monitor LLM API costs with Langfuse

## Security Considerations

- **Never commit `.env` files** - .gitignore handles this
- Use managed identities when deploying to Azure
- Rotate API keys regularly
- Monitor Langfuse for unusual LLM usage
- Consider rate limiting for public deployments

## Deployment

### Deploy to Streamlit Cloud

1. Push your code to GitHub (with .env in .gitignore)
2. Go to https://share.streamlit.io/
3. Connect your GitHub repo
4. Add secrets in Streamlit Cloud dashboard
5. Deploy!

### Deploy to Azure Container Apps

See `Dockerfile` configuration (if present) or use Azure Container Registry.

## License

[Your License Here - e.g., MIT]

## Contributing

Feel free to fork, submit issues, and create pull requests!

## Support

For issues or questions:
- Open a GitHub issue
- Check Azure documentation
- Review Streamlit docs at https://docs.streamlit.io

## Changelog

**v1.0.0** - Initial release
- Data upload and exploration
- Quality checks and profiling
- Interactive visualizations
- AI-powered insights
- ML recommendations
- Natural language queries

---
Application scrennshots:
<img width="1910" height="1030" alt="dashboard_landing page" src="https://github.com/user-attachments/assets/d47b6e6b-fcc1-483c-bd9b-fbfdb4a55f38" />

<img width="1898" height="1023" alt="dashboard_insights" src="https://github.com/user-attachments/assets/5f9badec-405e-4590-8831-68ace180c3d7" />


**Made using Streamlit and Azure AI**
