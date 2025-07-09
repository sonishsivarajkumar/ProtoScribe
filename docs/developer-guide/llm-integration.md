# LLM Integration

Deep dive into ProtoScribe's Large Language Model integration architecture, including multi-provider support, prompt engineering, and optimization strategies.

## Overview

ProtoScribe's LLM integration is designed with flexibility, reliability, and cost-effectiveness in mind. The system supports multiple AI providers with intelligent fallback mechanisms and sophisticated prompt engineering for clinical trial protocol analysis.

## Architecture

### Multi-Provider Framework

```python
# src/protoscribe/services/advanced_llm_analyzer.py

from abc import ABC, abstractmethod
from enum import Enum
from typing import Dict, List, Optional, Any

class LLMProvider(str, Enum):
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    AZURE_OPENAI = "azure_openai"

class BaseLLMProvider(ABC):
    """Abstract base class for all LLM providers"""
    
    @abstractmethod
    async def analyze_protocol(
        self, 
        content: str, 
        guidelines: List[str],
        analysis_type: str = "comprehensive"
    ) -> Dict[str, Any]:
        """Analyze protocol content and return structured results"""
        pass
    
    @abstractmethod
    async def check_availability(self) -> bool:
        """Check if the provider is currently available"""
        pass
    
    @abstractmethod
    def get_cost_per_token(self) -> Dict[str, float]:
        """Return cost per input/output token"""
        pass
```

### Provider Implementations

#### OpenAI Provider
```python
class OpenAIProvider(BaseLLMProvider):
    def __init__(self, api_key: str, model: str = "gpt-4"):
        self.client = OpenAI(api_key=api_key)
        self.model = model
        self.max_tokens = 4000
        self.temperature = 0.1  # Low temperature for consistency
    
    async def analyze_protocol(
        self, 
        content: str, 
        guidelines: List[str],
        analysis_type: str = "comprehensive"
    ) -> Dict[str, Any]:
        
        prompt = self._build_analysis_prompt(content, guidelines, analysis_type)
        
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self._get_system_prompt()},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                response_format={"type": "json_object"}
            )
            
            return self._parse_response(response.choices[0].message.content)
            
        except Exception as e:
            logger.error(f"OpenAI analysis failed: {e}")
            raise LLMProviderError(f"OpenAI analysis failed: {e}")
    
    def _build_analysis_prompt(
        self, 
        content: str, 
        guidelines: List[str], 
        analysis_type: str
    ) -> str:
        """Build context-aware analysis prompt"""
        
        guideline_content = self._load_guidelines(guidelines)
        
        if analysis_type == "comprehensive":
            return COMPREHENSIVE_ANALYSIS_TEMPLATE.format(
                protocol_content=content,
                consort_guidelines=guideline_content.get("consort", ""),
                spirit_guidelines=guideline_content.get("spirit", ""),
                analysis_instructions=self._get_comprehensive_instructions()
            )
        elif analysis_type == "clarity":
            return CLARITY_ANALYSIS_TEMPLATE.format(
                protocol_content=content,
                clarity_instructions=self._get_clarity_instructions()
            )
        elif analysis_type == "consistency":
            return CONSISTENCY_ANALYSIS_TEMPLATE.format(
                protocol_content=content,
                consistency_instructions=self._get_consistency_instructions()
            )
```

#### Anthropic Provider
```python
class AnthropicProvider(BaseLLMProvider):
    def __init__(self, api_key: str, model: str = "claude-3-opus-20240229"):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = model
        self.max_tokens = 4000
        self.temperature = 0.1
    
    async def analyze_protocol(
        self, 
        content: str, 
        guidelines: List[str],
        analysis_type: str = "comprehensive"
    ) -> Dict[str, Any]:
        
        prompt = self._build_anthropic_prompt(content, guidelines, analysis_type)
        
        try:
            response = await self.client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            return self._parse_response(response.content[0].text)
            
        except Exception as e:
            logger.error(f"Anthropic analysis failed: {e}")
            raise LLMProviderError(f"Anthropic analysis failed: {e}")
    
    def _build_anthropic_prompt(
        self, 
        content: str, 
        guidelines: List[str], 
        analysis_type: str
    ) -> str:
        """Build Anthropic-optimized prompt with clear structure"""
        
        return f"""
        <task>
        Analyze the following clinical trial protocol for compliance with {', '.join(guidelines)} guidelines.
        </task>

        <guidelines>
        {self._format_guidelines_for_anthropic(guidelines)}
        </guidelines>

        <protocol>
        {content}
        </protocol>

        <instructions>
        {self._get_anthropic_instructions(analysis_type)}
        </instructions>

        <output_format>
        Please provide your analysis in valid JSON format with the structure defined in the instructions.
        </output_format>
        """
```

### Intelligent Provider Selection

```python
class LLMManager:
    def __init__(self, providers: Dict[LLMProvider, BaseLLMProvider]):
        self.providers = providers
        self.provider_health = {}
        self.cost_tracker = CostTracker()
        self.performance_tracker = PerformanceTracker()
    
    async def select_optimal_provider(
        self, 
        analysis_type: str,
        content_length: int,
        user_preferences: Dict[str, Any] = None
    ) -> LLMProvider:
        """Select the best provider based on multiple factors"""
        
        # Check provider availability
        available_providers = []
        for provider_type, provider in self.providers.items():
            if await self._check_provider_health(provider_type, provider):
                available_providers.append(provider_type)
        
        if not available_providers:
            raise NoProvidersAvailableError("No LLM providers are currently available")
        
        # Score providers based on multiple criteria
        provider_scores = {}
        for provider_type in available_providers:
            score = await self._score_provider(
                provider_type, 
                analysis_type, 
                content_length, 
                user_preferences
            )
            provider_scores[provider_type] = score
        
        # Select highest scoring provider
        best_provider = max(provider_scores, key=provider_scores.get)
        logger.info(f"Selected provider: {best_provider} (score: {provider_scores[best_provider]})")
        
        return best_provider
    
    async def _score_provider(
        self, 
        provider_type: LLMProvider,
        analysis_type: str,
        content_length: int,
        user_preferences: Dict[str, Any]
    ) -> float:
        """Score provider based on performance, cost, and capabilities"""
        
        # Base scoring factors
        scores = {
            "availability": 1.0 if self.provider_health.get(provider_type, False) else 0.0,
            "performance": self.performance_tracker.get_success_rate(provider_type),
            "speed": 1.0 / max(self.performance_tracker.get_avg_response_time(provider_type), 1.0),
            "cost": 1.0 / max(self._estimate_cost(provider_type, content_length), 0.01),
            "capability": self._get_capability_score(provider_type, analysis_type)
        }
        
        # User preference weights
        weights = user_preferences.get("provider_weights", {
            "availability": 0.3,
            "performance": 0.25,
            "speed": 0.2,
            "cost": 0.15,
            "capability": 0.1
        })
        
        # Calculate weighted score
        total_score = sum(scores[factor] * weights.get(factor, 0) for factor in scores)
        return total_score
```

## Prompt Engineering

### Template System

```python
# Comprehensive analysis prompt template
COMPREHENSIVE_ANALYSIS_TEMPLATE = """
Analyze the following clinical trial protocol for compliance with CONSORT and SPIRIT guidelines.

PROTOCOL CONTENT:
{protocol_content}

CONSORT GUIDELINES:
{consort_guidelines}

SPIRIT GUIDELINES:
{spirit_guidelines}

ANALYSIS INSTRUCTIONS:
{analysis_instructions}

Please provide a comprehensive analysis in the following JSON format:

{{
  "overall_score": <0-100>,
  "consort_score": <0-100>,
  "spirit_score": <0-100>,
  "categories": {{
    "study_design": {{"score": <0-100>, "status": "excellent|good|needs_improvement|poor"}},
    "methodology": {{"score": <0-100>, "status": "excellent|good|needs_improvement|poor"}},
    "participants": {{"score": <0-100>, "status": "excellent|good|needs_improvement|poor"}},
    "interventions": {{"score": <0-100>, "status": "excellent|good|needs_improvement|poor"}},
    "outcomes": {{"score": <0-100>, "status": "excellent|good|needs_improvement|poor"}},
    "statistics": {{"score": <0-100>, "status": "excellent|good|needs_improvement|poor"}},
    "ethics": {{"score": <0-100>, "status": "excellent|good|needs_improvement|poor"}}
  }},
  "suggestions": [
    {{
      "section": "<protocol_section>",
      "type": "critical|improvement|style",
      "content": "<detailed_suggestion>",
      "confidence": <0.0-1.0>,
      "priority": "high|medium|low",
      "guideline_reference": "<CONSORT_item_X|SPIRIT_item_Y>",
      "rationale": "<explanation_for_suggestion>"
    }}
  ],
  "strengths": [
    "<positive_aspects_of_protocol>"
  ],
  "critical_issues": [
    "<must_fix_issues_for_compliance>"
  ]
}}
"""

# Clarity analysis prompt template
CLARITY_ANALYSIS_TEMPLATE = """
Analyze the clarity and readability of the following clinical trial protocol.

PROTOCOL CONTENT:
{protocol_content}

CLARITY ANALYSIS INSTRUCTIONS:
{clarity_instructions}

Focus on:
1. Language clarity and precision
2. Technical terminology usage
3. Sentence structure and readability
4. Logical flow and organization
5. Consistency in terminology

Provide analysis in JSON format:

{{
  "clarity_score": <0-100>,
  "readability": {{
    "grade_level": "<elementary|high_school|college|graduate>",
    "avg_sentence_length": <number>,
    "complex_words_ratio": <0.0-1.0>
  }},
  "language_issues": [
    {{
      "section": "<section_name>",
      "issue_type": "passive_voice|complex_sentences|unclear_terminology|inconsistent_usage",
      "description": "<issue_description>",
      "suggestion": "<improvement_suggestion>",
      "confidence": <0.0-1.0>
    }}
  ],
  "terminology": {{
    "consistency_score": <0-100>,
    "undefined_terms": ["<term1>", "<term2>"],
    "inconsistent_usage": [
      {{
        "term": "<term>",
        "variations": ["<variation1>", "<variation2>"],
        "recommended": "<preferred_usage>"
      }}
    ]
  }}
}}
"""
```

### Dynamic Prompt Construction

```python
class PromptBuilder:
    def __init__(self):
        self.templates = self._load_templates()
        self.guidelines = self._load_guidelines()
    
    def build_analysis_prompt(
        self, 
        content: str,
        analysis_type: str,
        guidelines: List[str],
        provider: LLMProvider,
        context: Dict[str, Any] = None
    ) -> str:
        """Build context-aware prompt for specific provider and analysis type"""
        
        # Select appropriate template
        template = self._select_template(analysis_type, provider)
        
        # Build context-specific instructions
        instructions = self._build_instructions(analysis_type, guidelines, context)
        
        # Format guideline content
        guideline_content = self._format_guidelines(guidelines, provider)
        
        # Apply provider-specific optimizations
        if provider == LLMProvider.ANTHROPIC:
            return self._optimize_for_anthropic(template, content, instructions, guideline_content)
        elif provider == LLMProvider.OPENAI:
            return self._optimize_for_openai(template, content, instructions, guideline_content)
        else:
            return template.format(
                protocol_content=content,
                analysis_instructions=instructions,
                **guideline_content
            )
    
    def _build_instructions(
        self, 
        analysis_type: str, 
        guidelines: List[str], 
        context: Dict[str, Any]
    ) -> str:
        """Build dynamic instructions based on analysis context"""
        
        base_instructions = self.templates[f"{analysis_type}_instructions"]
        
        # Add context-specific instructions
        if context:
            if context.get("study_phase"):
                base_instructions += f"\n\nSPECIAL FOCUS: This is a Phase {context['study_phase']} trial. Pay particular attention to {self._get_phase_specific_requirements(context['study_phase'])}."
            
            if context.get("therapeutic_area"):
                base_instructions += f"\n\nTHERAPEUTIC AREA: Consider {context['therapeutic_area']}-specific regulatory requirements and best practices."
            
            if context.get("regulatory_region"):
                base_instructions += f"\n\nREGULATORY CONTEXT: Focus on {context['regulatory_region']} regulatory requirements and submission standards."
        
        return base_instructions
    
    def _optimize_for_anthropic(
        self, 
        template: str, 
        content: str, 
        instructions: str, 
        guideline_content: Dict[str, str]
    ) -> str:
        """Optimize prompt structure for Anthropic models"""
        
        return f"""
        <role>
        You are an expert clinical research consultant specializing in regulatory compliance and protocol optimization.
        </role>

        <task>
        {instructions}
        </task>

        <guidelines>
        {self._format_guidelines_with_xml(guideline_content)}
        </guidelines>

        <protocol>
        {content}
        </protocol>

        <thinking>
        Before providing your analysis, think through:
        1. What are the key compliance requirements?
        2. Which sections of the protocol need the most attention?
        3. What are the critical vs. minor issues?
        4. How can the protocol be improved for regulatory approval?
        </thinking>

        <output>
        Provide your analysis in the exact JSON format specified in the task instructions.
        </output>
        """
```

## Response Processing

### Structured Output Parsing

```python
class ResponseParser:
    def __init__(self):
        self.validators = {
            "comprehensive": self._validate_comprehensive_response,
            "clarity": self._validate_clarity_response,
            "consistency": self._validate_consistency_response
        }
    
    def parse_response(
        self, 
        raw_response: str, 
        analysis_type: str,
        provider: LLMProvider
    ) -> Dict[str, Any]:
        """Parse and validate LLM response"""
        
        try:
            # Clean response (remove markdown formatting, etc.)
            cleaned_response = self._clean_response(raw_response, provider)
            
            # Parse JSON
            parsed_data = json.loads(cleaned_response)
            
            # Validate structure
            if analysis_type in self.validators:
                validated_data = self.validators[analysis_type](parsed_data)
            else:
                validated_data = parsed_data
            
            # Add metadata
            validated_data["_metadata"] = {
                "provider": provider.value,
                "analysis_type": analysis_type,
                "parsed_at": datetime.utcnow().isoformat(),
                "validation_status": "passed"
            }
            
            return validated_data
            
        except json.JSONDecodeError as e:
            logger.error(f"JSON parsing failed: {e}")
            return self._handle_parsing_error(raw_response, e)
        except ValidationError as e:
            logger.error(f"Response validation failed: {e}")
            return self._handle_validation_error(parsed_data, e)
    
    def _validate_comprehensive_response(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate comprehensive analysis response structure"""
        
        required_fields = [
            "overall_score", "consort_score", "spirit_score", 
            "categories", "suggestions", "strengths", "critical_issues"
        ]
        
        for field in required_fields:
            if field not in data:
                raise ValidationError(f"Missing required field: {field}")
        
        # Validate score ranges
        for score_field in ["overall_score", "consort_score", "spirit_score"]:
            score = data[score_field]
            if not isinstance(score, (int, float)) or not 0 <= score <= 100:
                raise ValidationError(f"Invalid score for {score_field}: {score}")
        
        # Validate suggestions structure
        for i, suggestion in enumerate(data.get("suggestions", [])):
            self._validate_suggestion_structure(suggestion, i)
        
        return data
    
    def _validate_suggestion_structure(self, suggestion: Dict[str, Any], index: int):
        """Validate individual suggestion structure"""
        
        required_fields = ["section", "type", "content", "confidence", "priority"]
        for field in required_fields:
            if field not in suggestion:
                raise ValidationError(f"Suggestion {index} missing field: {field}")
        
        # Validate suggestion type
        if suggestion["type"] not in ["critical", "improvement", "style"]:
            raise ValidationError(f"Invalid suggestion type: {suggestion['type']}")
        
        # Validate confidence score
        confidence = suggestion["confidence"]
        if not isinstance(confidence, (int, float)) or not 0.0 <= confidence <= 1.0:
            raise ValidationError(f"Invalid confidence score: {confidence}")
        
        # Validate priority
        if suggestion["priority"] not in ["high", "medium", "low"]:
            raise ValidationError(f"Invalid priority: {suggestion['priority']}")
```

## Performance Optimization

### Caching Strategy

```python
class LLMCache:
    def __init__(self, redis_url: str = None):
        self.redis_client = redis.from_url(redis_url) if redis_url else None
        self.local_cache = {}
        self.cache_ttl = 3600  # 1 hour
    
    def _generate_cache_key(
        self, 
        content: str, 
        analysis_type: str, 
        guidelines: List[str],
        provider: LLMProvider
    ) -> str:
        """Generate unique cache key for analysis request"""
        
        content_hash = hashlib.md5(content.encode()).hexdigest()
        params = f"{analysis_type}:{':'.join(sorted(guidelines))}:{provider.value}"
        return f"llm_analysis:{content_hash}:{params}"
    
    async def get_cached_result(
        self, 
        content: str, 
        analysis_type: str, 
        guidelines: List[str],
        provider: LLMProvider
    ) -> Optional[Dict[str, Any]]:
        """Retrieve cached analysis result"""
        
        cache_key = self._generate_cache_key(content, analysis_type, guidelines, provider)
        
        # Try Redis first
        if self.redis_client:
            try:
                cached_data = await self.redis_client.get(cache_key)
                if cached_data:
                    return json.loads(cached_data)
            except Exception as e:
                logger.warning(f"Redis cache retrieval failed: {e}")
        
        # Fallback to local cache
        return self.local_cache.get(cache_key)
    
    async def cache_result(
        self, 
        content: str, 
        analysis_type: str, 
        guidelines: List[str],
        provider: LLMProvider,
        result: Dict[str, Any]
    ):
        """Cache analysis result"""
        
        cache_key = self._generate_cache_key(content, analysis_type, guidelines, provider)
        serialized_result = json.dumps(result)
        
        # Cache in Redis
        if self.redis_client:
            try:
                await self.redis_client.setex(cache_key, self.cache_ttl, serialized_result)
            except Exception as e:
                logger.warning(f"Redis cache storage failed: {e}")
        
        # Cache locally
        self.local_cache[cache_key] = result
        
        # Implement local cache size limit
        if len(self.local_cache) > 100:
            # Remove oldest entries
            oldest_keys = list(self.local_cache.keys())[:20]
            for key in oldest_keys:
                del self.local_cache[key]
```

### Rate Limiting and Queue Management

```python
class RateLimiter:
    def __init__(self):
        self.provider_limits = {
            LLMProvider.OPENAI: {"rpm": 60, "tpm": 1000000},
            LLMProvider.ANTHROPIC: {"rpm": 50, "tpm": 800000},
            LLMProvider.AZURE_OPENAI: {"rpm": 120, "tpm": 2000000}
        }
        self.request_counts = defaultdict(lambda: defaultdict(int))
        self.token_counts = defaultdict(lambda: defaultdict(int))
    
    async def check_rate_limit(
        self, 
        provider: LLMProvider, 
        estimated_tokens: int
    ) -> bool:
        """Check if request is within rate limits"""
        
        current_minute = int(time.time() // 60)
        limits = self.provider_limits[provider]
        
        # Check request per minute limit
        if self.request_counts[provider][current_minute] >= limits["rpm"]:
            return False
        
        # Check tokens per minute limit
        if self.token_counts[provider][current_minute] + estimated_tokens > limits["tpm"]:
            return False
        
        return True
    
    async def record_request(
        self, 
        provider: LLMProvider, 
        actual_tokens: int
    ):
        """Record request for rate limiting"""
        
        current_minute = int(time.time() // 60)
        self.request_counts[provider][current_minute] += 1
        self.token_counts[provider][current_minute] += actual_tokens
        
        # Clean up old entries
        cutoff_minute = current_minute - 5
        for minute in list(self.request_counts[provider].keys()):
            if minute < cutoff_minute:
                del self.request_counts[provider][minute]
                del self.token_counts[provider][minute]

class AsyncAnalysisQueue:
    def __init__(self, max_concurrent: int = 5):
        self.queue = asyncio.Queue()
        self.active_tasks = set()
        self.max_concurrent = max_concurrent
        self.results = {}
    
    async def add_analysis_request(
        self, 
        request_id: str,
        analysis_request: Dict[str, Any]
    ) -> str:
        """Add analysis request to queue"""
        
        await self.queue.put((request_id, analysis_request))
        return request_id
    
    async def process_queue(self):
        """Process queued analysis requests"""
        
        while True:
            if len(self.active_tasks) < self.max_concurrent:
                try:
                    request_id, analysis_request = await asyncio.wait_for(
                        self.queue.get(), timeout=1.0
                    )
                    
                    task = asyncio.create_task(
                        self._process_analysis_request(request_id, analysis_request)
                    )
                    self.active_tasks.add(task)
                    task.add_done_callback(lambda t: self.active_tasks.discard(t))
                    
                except asyncio.TimeoutError:
                    continue
            else:
                await asyncio.sleep(0.1)
```

## Error Handling and Fallback

### Robust Error Handling

```python
class LLMError(Exception):
    """Base exception for LLM-related errors"""
    pass

class LLMProviderError(LLMError):
    """Error from specific LLM provider"""
    def __init__(self, provider: LLMProvider, message: str, details: Dict[str, Any] = None):
        super().__init__(message)
        self.provider = provider
        self.details = details or {}

class RateLimitError(LLMError):
    """Rate limit exceeded error"""
    def __init__(self, provider: LLMProvider, retry_after: int):
        super().__init__(f"Rate limit exceeded for {provider}")
        self.provider = provider
        self.retry_after = retry_after

class NoProvidersAvailableError(LLMError):
    """No providers available for analysis"""
    pass

class FallbackManager:
    def __init__(self, providers: Dict[LLMProvider, BaseLLMProvider]):
        self.providers = providers
        self.fallback_chains = {
            LLMProvider.OPENAI: [LLMProvider.ANTHROPIC, LLMProvider.AZURE_OPENAI],
            LLMProvider.ANTHROPIC: [LLMProvider.OPENAI, LLMProvider.AZURE_OPENAI],
            LLMProvider.AZURE_OPENAI: [LLMProvider.OPENAI, LLMProvider.ANTHROPIC]
        }
    
    async def analyze_with_fallback(
        self, 
        primary_provider: LLMProvider,
        content: str,
        guidelines: List[str],
        analysis_type: str
    ) -> Dict[str, Any]:
        """Attempt analysis with primary provider and fallback on failure"""
        
        providers_to_try = [primary_provider] + self.fallback_chains.get(primary_provider, [])
        last_error = None
        
        for provider_type in providers_to_try:
            if provider_type not in self.providers:
                continue
                
            provider = self.providers[provider_type]
            
            try:
                logger.info(f"Attempting analysis with {provider_type}")
                result = await provider.analyze_protocol(content, guidelines, analysis_type)
                
                # Add fallback information to result
                result["_metadata"] = result.get("_metadata", {})
                result["_metadata"]["primary_provider"] = primary_provider.value
                result["_metadata"]["actual_provider"] = provider_type.value
                result["_metadata"]["fallback_used"] = provider_type != primary_provider
                
                return result
                
            except Exception as e:
                last_error = e
                logger.warning(f"Analysis failed with {provider_type}: {e}")
                
                # Don't retry on certain error types
                if isinstance(e, (ValidationError, json.JSONDecodeError)):
                    break
                
                continue
        
        # All providers failed
        raise NoProvidersAvailableError(
            f"All providers failed. Last error: {last_error}"
        )
```

## Cost Optimization

### Token Estimation and Cost Tracking

```python
class CostTracker:
    def __init__(self):
        self.provider_costs = {
            LLMProvider.OPENAI: {
                "gpt-4": {"input": 0.03, "output": 0.06},  # per 1K tokens
                "gpt-4-turbo": {"input": 0.01, "output": 0.03}
            },
            LLMProvider.ANTHROPIC: {
                "claude-3-opus": {"input": 0.015, "output": 0.075},
                "claude-3-sonnet": {"input": 0.003, "output": 0.015}
            }
        }
        self.usage_history = []
    
    def estimate_cost(
        self, 
        provider: LLMProvider, 
        model: str,
        input_tokens: int, 
        estimated_output_tokens: int
    ) -> float:
        """Estimate cost for analysis request"""
        
        if provider not in self.provider_costs or model not in self.provider_costs[provider]:
            return 0.0
        
        costs = self.provider_costs[provider][model]
        input_cost = (input_tokens / 1000) * costs["input"]
        output_cost = (estimated_output_tokens / 1000) * costs["output"]
        
        return input_cost + output_cost
    
    def record_usage(
        self, 
        provider: LLMProvider,
        model: str,
        input_tokens: int,
        output_tokens: int,
        analysis_type: str
    ):
        """Record actual usage for cost tracking"""
        
        cost = self.estimate_cost(provider, model, input_tokens, output_tokens)
        
        usage_record = {
            "timestamp": datetime.utcnow(),
            "provider": provider.value,
            "model": model,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "total_tokens": input_tokens + output_tokens,
            "cost": cost,
            "analysis_type": analysis_type
        }
        
        self.usage_history.append(usage_record)
    
    def get_cost_summary(self, days: int = 30) -> Dict[str, Any]:
        """Get cost summary for specified period"""
        
        cutoff = datetime.utcnow() - timedelta(days=days)
        recent_usage = [
            record for record in self.usage_history 
            if record["timestamp"] > cutoff
        ]
        
        total_cost = sum(record["cost"] for record in recent_usage)
        total_tokens = sum(record["total_tokens"] for record in recent_usage)
        
        by_provider = {}
        for record in recent_usage:
            provider = record["provider"]
            if provider not in by_provider:
                by_provider[provider] = {"cost": 0, "tokens": 0, "requests": 0}
            
            by_provider[provider]["cost"] += record["cost"]
            by_provider[provider]["tokens"] += record["total_tokens"]
            by_provider[provider]["requests"] += 1
        
        return {
            "period_days": days,
            "total_cost": total_cost,
            "total_tokens": total_tokens,
            "total_requests": len(recent_usage),
            "avg_cost_per_request": total_cost / len(recent_usage) if recent_usage else 0,
            "by_provider": by_provider
        }
```

!!! tip "LLM Integration Best Practices"
    - Always implement fallback mechanisms for production reliability
    - Cache results to minimize costs and improve response times
    - Use appropriate temperature settings (low for consistency, higher for creativity)
    - Implement proper rate limiting to avoid API quota issues
    - Monitor costs and usage patterns regularly

!!! warning "Security Considerations"
    - Never log or expose API keys in plain text
    - Implement proper input sanitization before sending to LLMs
    - Be mindful of data privacy when using external AI services
    - Consider on-premises deployment for sensitive protocols

!!! info "Performance Tips"
    - Pre-process protocols to extract relevant sections for analysis
    - Use streaming responses for better user experience with long analyses
    - Implement request batching for multiple protocols
    - Consider fine-tuning models for domain-specific improvements
