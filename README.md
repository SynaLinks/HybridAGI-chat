# HybridAGI Streamlit App

![Alpha](https://img.shields.io/badge/Release-Alpha-orange)

Welcome to HybridAGI Streamlit app! This application allows you to interact with HybridAGI, in a user-friendly web interface built with [Streamlit](https://streamlit.io/).

## Getting Started

To get started with the HybridAGI Streamlit app, follow these simple steps:

### 1. Clone the Repository

First, clone this repository to your local machine using the following command:

```bash
git clone https://github.com/SynaLinks/HybridAGI-app.git
```

### 2. Set Up Your OpenAI API Key

Before running the app, you need to set up your OpenAI API key. 

- Rename the `.env.template` file to `.env`.

- Open the `.env` file in a text editor.

- Replace `my-openai-api-key` with your actual OpenAI API key.

### 3. Start the App

Navigate to the cloned repository:

```bash
cd HybridAGI-app
```

Now, you can start the app using Docker Compose:

```bash
docker-compose up
```

The app will build and run within a Docker container, and you'll see the Streamlit app URL in your terminal.

### 4. Access the App

Open a web browser and enter the Streamlit app URL. By default, it should be `http://localhost:8501`. You'll be able to interact with HybridAGI via this web interface.

## How to Use the App

The Streamlit app provides a simple and intuitive interface for interacting with HybridAGI.

You can:
- Input your objectives.
- Chat with the model
- Experiment with the program editor to see how the model responds.
- Get explaination about the behavior of the model.

Feel free to explore and test the capabilities of HybridAGI!

## Issues and Contributions

If you encounter any issues or have suggestions for improvements, please open an issue on the GitHub repository. Contributions are also welcome, so feel free to submit pull requests to enhance the app further.

Enjoy using the HybridAGI Streamlit app!
