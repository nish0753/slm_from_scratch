import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, HRFlowable, KeepTogether
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748B"))
        
        # Header (pages > 1)
        if self._pageNumber > 1:
            self.drawString(54, 750, "Small Language Model (SLM) from Scratch — Interview Guide")
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.5)
            self.line(54, 742, 558, 742)
            
        # Footer
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(558, 36, page_str)
        self.drawString(54, 36, "CONFIDENTIAL — Technical Interview Study Guide")
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.5)
        self.line(54, 48, 558, 48)
        self.restoreState()

def create_interview_pdf(filename):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )
    
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=colors.HexColor('#0F172A'),
        spaceAfter=6
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        leading=15,
        textColor=colors.HexColor('#475569'),
        spaceAfter=12
    )
    
    h1_style = ParagraphStyle(
        'SectionH1',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=19,
        textColor=colors.HexColor('#1E293B'),
        spaceBefore=14,
        spaceAfter=8,
        keepWithNext=True
    )
    
    h2_style = ParagraphStyle(
        'SectionH2',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11.5,
        leading=15,
        textColor=colors.HexColor('#2563EB'),
        spaceBefore=10,
        spaceAfter=5,
        keepWithNext=True
    )
    
    body_style = ParagraphStyle(
        'BodyTextCustom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor('#334155'),
        spaceAfter=5
    )
    
    bullet_style = ParagraphStyle(
        'BulletCustom',
        parent=body_style,
        leftIndent=12,
        bulletIndent=4,
        spaceAfter=4
    )

    script_quote_style = ParagraphStyle(
        'ScriptQuote',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor('#0F172A'),
        leftIndent=10,
        spaceAfter=6
    )

    code_style = ParagraphStyle(
        'CodeStyle',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=8,
        leading=11,
        textColor=colors.HexColor('#0F172A'),
        backColor=colors.HexColor('#F1F5F9'),
        borderColor=colors.HexColor('#E2E8F0'),
        borderWidth=0.5,
        borderPadding=5,
        spaceAfter=5
    )
    
    qa_box_style = ParagraphStyle(
        'QABoxQuestion',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=13,
        textColor=colors.HexColor('#1E3A8A'),
        spaceAfter=3
    )

    qa_answer_style = ParagraphStyle(
        'QABoxAnswer',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=12.5,
        textColor=colors.HexColor('#1E293B'),
        spaceAfter=5
    )

    story = []
    
    # ── COVER / TITLE SECTION ──────────────────────────────────────────────
    story.append(Paragraph("Small Language Model (SLM) from Scratch", title_style))
    story.append(Paragraph("<b>Complete Interview Walkthrough Script, Deep-Dive & Technical Q&A Guide</b>", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor('#2563EB'), spaceAfter=12))
    
    # ── SECTION 1: 5-MINUTE INTERVIEW WALKTHROUGH SCRIPT ────────────────────
    story.append(Paragraph("1. The 5-Minute Interview Walkthrough Script", h1_style))
    story.append(Paragraph("When asked <i>'Walk me through your Small Language Model project'</i>, use this structured narrative flow to demonstrate low-level architectural control and hardware awareness.", body_style))
    story.append(Spacer(1, 4))

    steps_data = [
        [Paragraph("<b>Phase & Time</b>", body_style), Paragraph("<b>What to Say (Exact Script)</b>", body_style), Paragraph("<b>Key Concept Highlighted</b>", body_style)],
        [
            Paragraph("<b>Step 1: High-Level Hook</b><br/>(0:00 - 0:30)", body_style),
            Paragraph("<i>'I built a ~10.8 Million parameter Small Language Model from scratch in PyTorch without high-level transformer libraries to master decoder-only LLM mechanics under the hood. It uses a context length of 256 tokens across 6 transformer blocks with 6 attention heads.'</i>", script_quote_style),
            Paragraph("PyTorch control & architecture scale", body_style)
        ],
        [
            Paragraph("<b>Step 2: Data Pipeline</b><br/>(0:30 - 1:30)", body_style),
            Paragraph("<i>'In prepare.py, I implemented regex text normalization and character tokenization. To optimize memory I/O, I serialized tokens into uint16 binary files (train.bin/val.bin). Because vocab_size is 75, uint16 cuts RAM/disk transfer bandwidth by 75% compared to 64-bit tensors.'</i>", script_quote_style),
            Paragraph("Hardware-conscious binary dataset optimization", body_style)
        ],
        [
            Paragraph("<b>Step 3: Model Architecture</b><br/>(1:30 - 3:30)", body_style),
            Paragraph("<i>'In model.py, token and positional embeddings are summed with dropout. Each block uses Pre-LayerNorm (x = x + Attn(LN(x))) for gradient stability. CausalSelfAttention computes Q, K, V in one projection and applies a lower-triangular -inf mask. I also added Weight Tying between token embeddings and the output head.'</i>", script_quote_style),
            Paragraph("Pre-LN, Causal Masking, GELU & Weight Tying", body_style)
        ],
        [
            Paragraph("<b>Step 4: Training Engine</b><br/>(3:30 - 4:30)", body_style),
            Paragraph("<i>'In train.py, batches are sampled using torch.randint from binary files. I trained with AdamW (lr=3e-4) over 5,000 steps, evaluating train/val loss every 500 steps under @torch.no_grad(), saving checkpoints to base_model.pt.'</i>", script_quote_style),
            Paragraph("AdamW optimization & no_grad evaluation", body_style)
        ],
        [
            Paragraph("<b>Step 5: Generation & Vision</b><br/>(4:30 - 5:00)", body_style),
            Paragraph("<i>'In generate.py, text generation crops prompts to 256 tokens, applies temperature scaling (logits / T), and samples via torch.multinomial. Next, I plan to upgrade to FlashAttention 2 and Top-P (nucleus) sampling.'</i>", script_quote_style),
            Paragraph("Temperature sampling & production roadmap", body_style)
        ]
    ]

    walkthrough_table = Table(steps_data, colWidths=[90, 294, 120])
    walkthrough_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#F1F5F9')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.HexColor('#0F172A')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(walkthrough_table)
    story.append(Spacer(1, 10))

    # ── SECTION 2: ARCHITECTURAL OVERVIEW & SPECS ──────────────────────────
    story.append(Paragraph("2. Architectural Overview & Specifications", h1_style))
    
    specs_data = [
        [Paragraph("<b>Component</b>", body_style), Paragraph("<b>Specification / Value</b>", body_style), Paragraph("<b>Technical Justification</b>", body_style)],
        [Paragraph("Model Type", body_style), Paragraph("Decoder-only Autoregressive Transformer", body_style), Paragraph("Generates text token-by-token using causal masking.", body_style)],
        [Paragraph("Parameters", body_style), Paragraph("~10.8M parameters", body_style), Paragraph("Compact SLM suitable for CPU/single-GPU training.", body_style)],
        [Paragraph("Embedding Dimension (n_embd)", body_style), Paragraph("384", body_style), Paragraph("Dense vector size per token representation.", body_style)],
        [Paragraph("Attention Heads (n_head)", body_style), Paragraph("6 heads (head_dim = 64)", body_style), Paragraph("Multi-Head Attention projects into 6 parallel subspaces.", body_style)],
        [Paragraph("Transformer Layers (n_layer)", body_style), Paragraph("6 Blocks", body_style), Paragraph("Stacked pre-LayerNorm residual block layers.", body_style)],
        [Paragraph("Context Window (block_size)", body_style), Paragraph("256 tokens", body_style), Paragraph("Maximum sequence length for causal attention.", body_style)],
        [Paragraph("Vocabulary Size", body_style), Paragraph("75 unique characters", body_style), Paragraph("Character-level tokenization built from input corpus.", body_style)],
        [Paragraph("Weight Tying", body_style), Paragraph("Enabled (tok_emb.weight = lm_head.weight)", body_style), Paragraph("Reduces parameter count and regularizes representation.", body_style)]
    ]
    
    spec_table = Table(specs_data, colWidths=[110, 160, 234])
    spec_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#F8FAFC')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.HexColor('#0F172A')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('TOPPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(spec_table)
    
    story.append(PageBreak())
    
    # ── SECTION 3: FILE-BY-FILE DEEP DIVE ─────────────────────────────────
    story.append(Paragraph("3. File-by-File Codebase Deep Dive", h1_style))
    
    # config.py
    story.append(Paragraph("File 1: config.py (Hyper-parameter Configuration)", h2_style))
    story.append(Paragraph("Uses Python dataclasses to cleanly separate model dimensions (<code>GPTConfig</code>) from training parameters (<code>TrainConfig</code>).", body_style))
    story.append(Paragraph("<code>@dataclass<br/>class GPTConfig:<br/>&nbsp;&nbsp;&nbsp;&nbsp;vocab_size: int = 75<br/>&nbsp;&nbsp;&nbsp;&nbsp;block_size: int = 256<br/>&nbsp;&nbsp;&nbsp;&nbsp;n_layer: int = 6<br/>&nbsp;&nbsp;&nbsp;&nbsp;n_head: int = 6<br/>&nbsp;&nbsp;&nbsp;&nbsp;n_embd: int = 384<br/>&nbsp;&nbsp;&nbsp;&nbsp;dropout: float = 0.2</code>", code_style))
    
    # prepare.py
    story.append(Paragraph("File 2: prepare.py (Data Ingestion & Tokenization)", h2_style))
    story.append(Paragraph("Cleans raw text with regex, constructs character lookup tables (<code>stoi</code> & <code>itos</code>), encodes text into integer tokens, and serializes arrays to disk in <code>uint16</code> format.", body_style))
    story.append(Paragraph("• <b>Regex Cleaning:</b> Strips Project Gutenberg metadata, normalizes brackets, and sanitizes stage direction artifacts.", bullet_style))
    story.append(Paragraph("• <b>uint16 Data Format:</b> Vocab size of 75 fits inside uint16 (0–65,535), saving 75% RAM/disk transfer bandwidth compared to 64-bit tensors.", bullet_style))
    story.append(Paragraph("• <b>90/10 Split:</b> Generates contiguous <code>train.bin</code> (~9.5MB) and <code>val.bin</code> (~1.0MB) files.", bullet_style))
    
    # model.py
    story.append(Paragraph("File 3: model.py (Core GPT Architecture)", h2_style))
    model_components = [
        ("CausalSelfAttention", "Computes Query, Key, and Value projections in a single matrix multiplication (Linear(n_embd, 3*n_embd)). Reshapes into (B, n_head, T, head_dim) and applies a lower-triangular mask (torch.tril) so tokens only attend to past positions: attn = softmax((Q @ K.T) / sqrt(d_k))."),
        ("FeedForward", "Expands representation dimension by 4x (Linear(n_embd, 4*n_embd)), applies GELU activation, projects back (Linear(4*n_embd, n_embd)), and applies dropout."),
        ("Block (Pre-LN Residual Block)", "Uses Pre-LayerNorm order: x = x + Attention(LayerNorm(x)), followed by x = x + FFN(LayerNorm(x)). Pre-LN provides stable gradient flow during backpropagation compared to Post-LN."),
        ("GPT & Weight Tying", "Combines Token Embeddings and Learned Positional Embeddings. Shares weights between token embeddings and the output head: tok_emb.weight = lm_head.weight (Weight Tying).")
    ]
    for comp_title, comp_desc in model_components:
        story.append(Paragraph(f"• <b>{comp_title}:</b> {comp_desc}", bullet_style))
        
    story.append(Spacer(1, 4))
    
    # train.py & generate.py
    story.append(Paragraph("File 4 & 5: train.py & generate.py", h2_style))
    story.append(Paragraph("• <b>train.py:</b> Samples batches via <code>torch.randint</code>, optimizes with <b>AdamW</b> (`lr=3e-4`), evaluates train/val loss under <code>@torch.no_grad()</code> every 500 steps, and saves <code>checkpoints/base_model.pt</code>.", bullet_style))
    story.append(Paragraph("• <b>generate.py:</b> Crops prompt context to 256 tokens, scales logits by temperature ($z / T$), applies Softmax, and samples via <code>torch.multinomial</code>.", bullet_style))

    story.append(PageBreak())
    
    # ── SECTION 4: INTERVIEW CROSS-QUESTIONS & ANSWERS ─────────────────────
    story.append(Paragraph("4. 15 Technical Interview Cross-Questions & Answers", h1_style))
    story.append(Paragraph("Below are 15 rigorous technical interview questions you may be asked regarding this implementation, complete with logical answers.", body_style))
    story.append(Spacer(1, 4))
    
    qa_list = [
        ("Q1: Why did you choose a Decoder-only Transformer architecture instead of Encoder-Decoder (like T5) or Encoder-only (like BERT)?",
         "Decoder-only architectures (e.g. GPT series, LLaMA) are optimal for autoregressive generative tasks because every token is predicted conditioned strictly on preceding tokens. Encoder-Decoder models are designed for sequence-to-sequence translation tasks, while Encoder-only models utilize bidirectional attention, making them suitable for classification/embedding tasks but incapable of efficient causal next-token generation."),

        ("Q2: Why do we divide the dot product (Q @ K^T) by sqrt(head_dim) in Self-Attention?",
         "For high embedding dimensions (e.g. head_dim = 64), the variance of dot products scales linearly with dimension. Without scaling by 1/sqrt(d_k), dot product values grow large in magnitude, pushing the Softmax function into regions with extremely small gradients (vanishing gradient problem). Scaling keeps variance at ~1.0, preserving healthy gradient flow."),

        ("Q3: What is Pre-LayerNorm vs Post-LayerNorm, and why does your model use Pre-LN?",
         "In Post-LN (used in original 2017 Transformer), LayerNorm is applied after the residual addition: x = LayerNorm(x + SubLayer(x)). This causes gradients at early layers to be unnormalized, requiring strict warm-up learning rates. Pre-LN applies LayerNorm before the sub-layer: x = x + SubLayer(LayerNorm(x)). Gradient flow through the residual skip connection remains uninhibited, ensuring numerical stability in deep networks."),

        ("Q4: Explain Weight Tying (tok_emb.weight = lm_head.weight). What are its benefits?",
         "Weight Tying forces the token embedding matrix and the output projection head to share the exact same weights tensor. Since token embeddings map discrete token IDs -> continuous vectors, and lm_head maps continuous vectors -> token logits, they perform inverse operations. Weight Tying reduces total model parameters significantly (~30% saving on large vocabularies) and prevents overfitting."),

        ("Q5: How does the causal attention mask work in PyTorch?",
         "A lower-triangular matrix of ones (torch.tril) is created. Positions where the mask is 0 (future tokens) are filled with negative infinity (-inf) prior to Softmax via masked_fill. Softmax(-inf) evaluates to exactly 0.0, ensuring token position i receives 0.0 attention weight from any future position j > i."),

        ("Q6: Why did you use AdamW instead of standard Adam or SGD?",
         "In standard Adam, L2 weight decay is added directly to gradients before computing exponential moving averages of first/second moments. For adaptive learning rate algorithms, this causes parameters with large historical gradients to be decayed less than those with small gradients. AdamW decouples weight decay from gradient moment updates, applying uniform decay directly to parameters."),

        ("Q7: What is the difference between character-level and subword tokenization (BPE/Tiktoken)?",
         "Character tokenization results in a tiny vocabulary size (75 vs 32,000+ in BPE), eliminating out-of-vocabulary errors without needing complex tokenizers. However, sequence lengths T are much longer for the same text (words take multiple characters), making self-attention compute (O(T^2)) significantly more expensive per word than subword BPE."),

        ("Q8: Why did you save data as uint16 binary files in prepare.py?",
         "PyTorch default integer tensors use int64 (8 bytes per token). Since our character vocabulary size is 75, token IDs range between 0 and 74, which fits inside uint16 (0 to 65,535; 2 bytes per token). Using uint16 reduces disk storage and RAM/disk transfer bandwidth by 75%."),

        ("Q9: What is the role of Temperature in generate.py?",
         "Temperature scales logits prior to Softmax: logits_scaled = logits / T. When T < 1.0, high-probability tokens become even more dominant (sharper distribution, deterministic text). When T > 1.0, the probability distribution flattens (higher entropy, more diverse/creative sampling)."),

        ("Q10: Why do we use GELU activation instead of ReLU in the Feed-Forward Network?",
         "ReLU drops all negative values to zero strictly, causing 'dead neuron' problems during backpropagation. GELU (Gaussian Error Linear Unit) weighs inputs by their probability under a Gaussian distribution, providing a smooth continuous curve for negative values and improving gradient performance in Transformer architectures."),

        ("Q11: What is the computational complexity of Self-Attention with respect to context length T?",
         "Self-attention scales quadratically in time and memory: O(T^2 * d_k). This is because every token in a sequence of length T calculates an attention score with every other token in the sequence (forming a T x T attention matrix)."),

        ("Q12: Why are Positional Embeddings required in Transformers?",
         "Self-attention is completely permutation-invariant — it computes set operations over tokens. Without positional embeddings (pos_emb), the model cannot distinguish between 'dog bites man' and 'man bites dog'. Adding positional vectors injects sequence order information into token representations."),

        ("Q13: What happens if a user inputs an out-of-vocabulary character in generate.py?",
         "In the current implementation, python throws a KeyError because character-level stoi lookup fails. To fix this in production, we should introduce an unknown fallback token '<unk>' (e.g. mapped to index 0) or filter input characters against known vocabulary."),

        ("Q14: What is FlashAttention, and why would you add it in a future version?",
         "Standard attention materializes the intermediate T x T attention matrix in High-Bandwidth Memory (HBM). FlashAttention reorganizes attention computation into tiled blocks executed entirely within fast GPU SRAM memory, avoiding HBM read/write bottlenecks and providing a 2x-4x speedup with exact attention precision."),

        ("Q15: How would you scale training of this SLM across multiple GPUs?",
         "For small models, Distributed Data Parallel (DDP) replicates the model across GPUs and averages gradients via AllReduce. For giant models that do not fit on a single GPU's VRAM, Fully Sharded Data Parallel (FSDP) or Tensor Parallelism (Megatron-LM) shards model weights, gradients, and optimizer states across devices.")
    ]
    
    for q_text, a_text in qa_list:
        qa_data = [
            [Paragraph(q_text, qa_box_style)],
            [Paragraph(a_text, qa_answer_style)]
        ]
        qa_table = Table(qa_data, colWidths=[504])
        qa_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#EFF6FF')),
            ('BACKGROUND', (0,1), (-1,1), colors.HexColor('#FFFFFF')),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#BFDBFE')),
            ('TOPPADDING', (0,0), (-1,-1), 4),
            ('BOTTOMPADDING', (0,0), (-1,-1), 4),
            ('LEFTPADDING', (0,0), (-1,-1), 8),
            ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ]))
        story.append(qa_table)
        story.append(Spacer(1, 5))

    story.append(PageBreak())
    
    # ── SECTION 5: FUTURE IMPROVEMENTS ROADMAP ──────────────────────────────
    story.append(Paragraph("5. Production & Architectural Enhancement Roadmap", h1_style))
    story.append(Paragraph("To demonstrate senior ML engineering vision during an interview, highlight these key technical upgrades you plan to integrate:", body_style))
    
    roadmap_data = [
        [Paragraph("<b>Enhancement</b>", body_style), Paragraph("<b>Target Area</b>", body_style), Paragraph("<b>Technical Impact & Benefit</b>", body_style)],
        [Paragraph("FlashAttention 2", body_style), Paragraph("Model Attention Block", body_style), Paragraph("Replaces custom Q@K.T with <code>torch.nn.functional.scaled_dot_product_attention</code>, accelerating attention by 2x-4x.", body_style)],
        [Paragraph("Rotary Position Embeddings (RoPE)", body_style), Paragraph("Positional Encoding", body_style), Paragraph("Replaces absolute learned embeddings with relative rotational embeddings for superior length extrapolation.", body_style)],
        [Paragraph("Subword BPE Tokenizer", body_style), Paragraph("Tokenization", body_style), Paragraph("Uses <code>tiktoken</code> or <code>sentencepiece</code> to shrink sequence length T per sentence, reducing O(T^2) attention compute.", body_style)],
        [Paragraph("Mixed Precision (AMP)", body_style), Paragraph("Training Loop", body_style), Paragraph("Uses <code>torch.amp.autocast(dtype=torch.bfloat16)</code> for 2x faster matrix multiplications on modern GPUs.", body_style)],
        [Paragraph("Cosine Annealing LR + Warmup", body_style), Paragraph("Optimization", body_style), Paragraph("Replaces constant learning rate with linear warmup and cosine decay to reach lower validation perplexity.", body_style)],
        [Paragraph("Top-K & Top-P (Nucleus) Sampling", body_style), Paragraph("Inference Engine", body_style), Paragraph("Truncates low-probability tail tokens in <code>generate.py</code>, eliminating repetitive text loops and gibberish.", body_style)]
    ]
    
    roadmap_table = Table(roadmap_data, colWidths=[130, 120, 254])
    roadmap_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#F8FAFC')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.HexColor('#0F172A')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('TOPPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(roadmap_table)
    
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully generated PDF: {filename}")

if __name__ == '__main__':
    create_interview_pdf("SLM_Project_Interview_Guide.pdf")
