#!/usr/bin/env python3

"""
Training Script for Minesweeper (2 GPUs)

Terminal 1 - Start vLLM server:

  CUDA_VISIBLE_DEVICES=0,1,2,3 vf-vllm \
      --model Qwen/Qwen2.5-14B-Instruct \
      --data-parallel-size 4 \
      --enforce-eager \
      --disable-log-requests

  Terminal 2 - Run training:

  CUDA_VISIBLE_DEVICES=4,5,6,7 uv run accelerate launch --config_file configs/default_config.yaml --num_processes 4 train.py

rm -rf ~/.triton ~/.cache/torch/inductor ~/.cache/torch/extension_cache
"""
import verifiers as vf

def main():
    env = vf.load_environment(
        env_id="hud-vf-gym",
        taskset="kizro/deep_research_taskset-50rows_filtered",  
        config_path="./configs/deepresearch.yaml",
    )
    
    # 2. Load model and tokenizer
    model_name = "Qwen/Qwen2.5-14B-Instruct"
    model, tokenizer = vf.get_model_and_tokenizer(model_name)
    
    # 3. Configure training using grpo_defaults
    args = vf.grpo_defaults(
        run_name="deepresearch-grpo"
    )

    args.max_steps = 1000
    args.save_strategy = "steps"
    args.save_steps = 20
    args.logging_steps = 1
    args.mask_env_responses = True
    args.max_prompt_length = 4096
    args.beta = 0   
    
    args.per_device_train_batch_size = 16  
    args.num_generations = 16    
    args.gradient_accumulation_steps = 2
    args.max_grad_norm = 0.003
    args.learning_rate = 5e-5
    
    # Memory optimization settings
    args.gradient_checkpointing = True
    args.fp16 = False
    args.bf16 = True

    # 4. Train
    trainer = vf.GRPOTrainer(
        model=model,
        processing_class=tokenizer,
        env=env,
        args=args,
        peft_config=vf.lora_defaults(r=8, alpha=16)
    )
    
    # Start training
    print("Starting GRPO training for Minesweeper with vLLM...")
    print(f"Model: {model_name}")
    
    trainer.train()
    
    # Save the final model
    trainer.save_model()
    print(f"\nTraining completed! Model saved to {args.output_dir}")

if __name__ == "__main__":
    main()
