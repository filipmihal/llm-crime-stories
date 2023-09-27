import os
import torch
import transformers
from torch import bfloat16, cuda
from transformers import StoppingCriteria, StoppingCriteriaList

class Llama:
    def __init__(self):
        model_id = "meta-llama/Llama-2-70b-chat-hf"

        device = f"cuda:{cuda.current_device()}" if cuda.is_available() else "cpu"

        # set quantization configuration to load large model with less GPU memory
        # this requires the `bitsandbytes` library
        bnb_config = transformers.BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_use_double_quant=True,
            bnb_4bit_compute_dtype=bfloat16,
        )

        # begin initializing HF items, you need an access token
        hf_auth = os.environ["HF_AUTH"]
        model_config = transformers.AutoConfig.from_pretrained(model_id, use_auth_token=hf_auth)

        model = transformers.AutoModelForCausalLM.from_pretrained(
            model_id,
            trust_remote_code=True,
            config=model_config,
            quantization_config=bnb_config,
            device_map="auto",
            use_auth_token=hf_auth,
        )

        # enable evaluation mode to allow model inference
        model.eval()

        print(f"Model loaded on {device}")

        tokenizer = transformers.AutoTokenizer.from_pretrained(model_id, use_auth_token=hf_auth)

        stop_list = ["\nHuman:", "\n```\n"]

        stop_token_ids = [tokenizer(x)["input_ids"] for x in stop_list]
        stop_token_ids = [torch.LongTensor(x).to(device) for x in stop_token_ids]


        # define custom stopping criteria object
        class StopOnTokens(StoppingCriteria):
            def __call__(
                self, input_ids: torch.LongTensor, scores: torch.FloatTensor, **kwargs
            ) -> bool:
                for stop_ids in stop_token_ids:
                    if torch.eq(input_ids[0][-len(stop_ids) :], stop_ids).all():
                        return True
                return False


        stopping_criteria = StoppingCriteriaList([StopOnTokens()])

        self._generate_text = transformers.pipeline(
            model=model,
            tokenizer=tokenizer,
            task="text-generation",
            # we pass model parameters here too
            stopping_criteria=stopping_criteria,  # without this model rambles during chat
            temperature=0.2,  # 'randomness' of outputs, 0.0 is the min and 1.0 the max
            max_new_tokens=4096,  # max number of tokens to generate in the output
            repetition_penalty=1.2,  # without this output begins repeating
        )
        
    @property
    def pipeline(self):
        return self._generate_text