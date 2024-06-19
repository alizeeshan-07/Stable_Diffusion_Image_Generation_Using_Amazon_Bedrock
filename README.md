# Stable_Diffusion_Image_Generation_Using_Amazon_Bedrock

This project demonstrates how to use the Stable Diffusion model via the AWS Bedrock service to generate a 4K HD image of a beach with a blue sky, rainy season, and cinematic display. The project involves setting up AWS CLI, configuring the necessary environment, and running a Python script to invoke the model.

## Prerequisites

Before running this script, ensure you have the following:

- Python 3.6 or higher
- AWS SDK for Python (`boto3`)
- AWS credentials configured with necessary permissions to use Bedrock service

## Installation

1. **Install boto3**:

    ```bash
    pip install boto3
    ```

2. **Configure AWS credentials**:

    Ensure your AWS credentials are configured. You can do this by setting up the `~/.aws/credentials` file or by using environment variables.

## Usage

1. **Script Overview**:

    This script sends a prompt to the Stable Diffusion API and receives an image in response. The prompt asks the model to generate a 4K HD image of a beach with specific conditions.

2. **Script Execution**:

    ```python
    import boto3
    import json
    import base64
    import os

    prompt_data = """
    provide me an 4K hd image of a beach, also use a blue sky rainy season and cinematic display
    """

    prompt_template = [{"text":prompt_data, "weight":1}]

    bedrock = boto3.client(service_name="bedrock-runtime")

    payload= {
        "text_prompts":prompt_template,
        "cfg_scale": 10,
        "seed": 0,
        "steps": 50,
        "width": 1024,
        "height":1024
    }

    body = json.dumps(payload)
    model_id = "stability.stable-diffusion-xl-v1"
    response = bedrock.invoke_model(
        body=body,
        modelId=model_id,
        accept='application/json', # can be commented
        contentType='application/json' # can be commented
    )

    response_body = json.loads(response.get("body").read())
    # print(response_body)

    artifact = response_body.get("artifacts")[0]
    image_encoded = artifact.get("base64").encode("utf-8")
    image_bytes = base64.b64decode(image_encoded)

    output_dir = "SD_output"
    os.makedirs(output_dir, exist_ok=True)
    file_name = f"{output_dir}/generated-image.png"
    with open(file_name, "wb") as f:
        f.write(image_bytes)
    ```

3. **Parameters**:

    - `prompt_data`: The input prompt for the Stable Diffusion API.
    - `cfg_scale`: Classifier-free guidance scale.
    - `seed`: Seed for random number generator to ensure reproducibility.
    - `steps`: Number of steps to generate the image.
    - `width`: Width of the generated image.
    - `height`: Height of the generated image.
    - `model_id`: The ID of the model to be used (`stability.stable-diffusion-xl-v1` by default).

4. **Running the Script**:

    To run the script, execute the following command:

    ```bash
    python app.py
    ```

    Replace `app.py` with the name of your Python file containing the above code.

## Notes

- The script uses the `stability.stable-diffusion-xl-v1` model by default. You can switch to a different model by updating the `model_id`.
- The `accept` and `contentType` parameters can be commented out if not required.

## Example Output

After running the script, you should see a generated image saved in the `SD_output` directory.

## Troubleshooting

- Ensure that your AWS credentials are correctly configured.
- Verify that you have the necessary permissions to access the Bedrock service.
- Check for any network connectivity issues that may prevent reaching the AWS services.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please submit a pull request or open an issue to discuss your ideas.
