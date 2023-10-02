from typing import Dict, List
import openai
from openai.error import APIConnectionError, APIError, RateLimitError
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_random_exponential


###########################################################
### REVIEW HELPER ###
###########################################################

def auto_improve_prompt():
    return """
       Automatically enhance the provided review using an "Auto-Improve" mechanism, ensuring the refined review adheres to high-quality standards pertaining to grammar, style, coherence, and more.

        Characteristics of Auto-Improve:
        1. Automated Enhancement: Utilize technology and predefined rules for review improvement.

        2. Grammar & Spelling: Ensure error-free review with consistent grammar.

        3. Stylistic Improvement: Enhance vocabulary and sentence structures.

        4. Coherence & Logic: Maintain logical flow and smooth transitions.

        5. Readability: Ensure the review is easy to read and understand.

        6. Format & Structure: Optimize paragraphs, and potentially headings.

        7. Punctuation: Correct punctuation usage.

        8. Consistency: Maintain style and voice consistency.

        9. Inclusivity: Use neutral and inclusive language.

        10. Legal & Ethical Compliance: Ensure adherence to applicable legal and ethical guidelines.
    """

def shorten_prompt():
    return """
        Revise the provided review with the objective to "Shorten" it, ensuring that the review is condensed while preserving its key messages, crucial information, and overall clarity.

        Characteristics of Shorten:
        1. Conciseness: Remove redundancy and utilize concise phrases.

        2. Preserving Meaning: Maintain key points and crucial information.

        3. Clarity: Ensure clear communication with simple language.

        4. Readability: Maintain easy reading and logical flow.
        
        5. Attention to Key Sections: Ensure clarity and completeness in key sections of the review.
    """ 

def expand_prompt():
    return """
        Revise the provided review with the objective to "Expand" it, ensuring that additional depth, detail, and content are added while maintaining clarity, coherence, and engagement.

        Characteristics of Expand:
        1. Elaboration: Add details, explanations, and additional information.

        2. Depth: Provide deeper analysis and explore multiple perspectives.

        3. Clarity and Coherence: Maintain clear transitions and logical flow.

        4. Supporting Evidence: Integrate citations, data, and statistics.

        5. Engagement: Ensure language is engaging.

        6. Formatting: Utilize subheadings and structured paragraphs.

        7. Relevance: Ensure all additions are relevant and avoid filler.
    """ 

def professional_tone_prompt():
    return """
        Improve the provided review to embody a Professional Tone adhering to the characteristics outlined below.

        Characteristics of a Professional Tone:
        1. Formality: Employ formal language, avoiding slang or colloquialisms. Utilize formal address, greetings, and closings.

        2. Clarity and Conciseness: Ensure directness and brevity, avoiding unnecessary elaboration or redundancy.

        3. Correctness: Vigilantly check for grammatical, spelling, and punctuation accuracy.
        
        4. Impersonality: Favor a third-person perspective and maintain objectivity by focusing on facts and data.
        
        5. Respectfulness and Politeness: Exhibit politeness and consider different perspectives respectfully.
        
        6. Specificity: Employ precise language, supported by relevant and accurate data or examples.
        
        7. Organized Structure: Ensure a logical flow of information, utilizing headings and subheadings for clear organization.
        
        8. Use of Jargon: Integrate industry-related terminology judiciously and appropriately.
        
        9. Neutral Vocabulary: Opt for neutral words and abstain from using emotionally charged language.
        
        10. Citations and References: Accurately credit sources and utilize reliable references.
        
        11. Legal & Ethical Compliance: Ensure adherence to applicable legal and ethical guidelines.
        
        12. Inclusivity: Employ language that is inclusive and non-discriminatory.
    """

def persuasive_tone_prompt():
    return """
        Revise or craft the provided review to embody a "Persuasive Tone," ensuring that the content is compelling and aims to influence the reader’s thoughts, feelings, or actions effectively.

        Characteristics of Persuasive Tone:
        1. Appealing Language: Employ emotive and positive language.

        2. Rhetorical Techniques: Utilize rhetorical questions and tripling.

        3. Logical Argumentation: Ensure a clear thesis supported by evidence.

        4. Addressing Counterarguments: Acknowledge and rebut opposing views.

        5. Call to Action: Include a compelling and urgent call to action.

        6. Credibility and Trust: Ensure credibility through expert quotes and ethical appeal.

        7. Engaging the Audience: Directly address and relate to the reader.

        8. Storytelling: Utilize anecdotes and scenarios to enhance emotional appeal.
    """ 

def fix_mistakes_only_prompt():
    return """
        Revise the provided review with the sole intention of "Fixing Mistakes Only," ensuring that all errors or mistakes within the review are corrected without altering the original style, tone, or meaning of the content.

        Characteristics of Fix Mistakes Only:
        1. Grammar Corrections: Ensure spelling, punctuation, and syntax are error-free.

        2. Accuracy: Verify the accuracy of facts, data, figures, and citations.

        3. Consistency: Maintain consistency in tense and style use.

        4. Readability: Correct sentence fragments and run-on sentences.

        5. Legal & Ethical Compliance: Ensure claims are legitimate and language is non-discriminatory.
        
        6. Language Appropriateness: Ensure appropriate and correct word usage.
    """


def review_prompt_messages(user_review: str, review_type: str) -> List[Dict]:
    # Craft the list of messages that will be sent to the model to instruct summarization.


    prompt_type_dict = {
        "Auto-Improve": auto_improve_prompt(),
        "Shorten":shorten_prompt(),
        "Expand":expand_prompt(),
        "Professional Tone": professional_tone_prompt(),
        "Persuasive Tone":persuasive_tone_prompt(),
        "Fix Mistakes Only":fix_mistakes_only_prompt()
    }

    return [
        {"role": "system", 
        "content": """
                You will receive a review from the user and a customization or style in which to help you model and improve 
                the review in.
                Evaluate the context from the review provided and provide an improved review in the style and customization
                asked by the user.
                Prioritize offering information and context provided within the review and do not convey any potentially false information.
                Strive to make your review as detailed as possible. 
                Respond in precise detail, directly repeating the information that you're referencing from the review provided.
                The user will only see your improved review and not the context you've been provided. 
                The review should not exceed more than 200 words.
        """},
        {"role": "user", 
        "content": f"""
                Improve the following review with the style or customization provided:
                Review: {user_review}
                Customization or style provided: {review_type}. 
                Objective: {prompt_type_dict[review_type]}
                Desired Output format: A single string object containing the improved review. The string should not be more than 200 words.
        """}
    ]


@retry(
    wait=wait_random_exponential(multiplier=1, max=30),
    stop=stop_after_attempt(3),
    retry=retry_if_exception_type(APIConnectionError) | retry_if_exception_type(APIError) | retry_if_exception_type(RateLimitError),
)
def gpt_improved_reviews(user_review: str, review_type: str):
    response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=review_prompt_messages(user_review=user_review, 
                                            review_type=review_type)
        )

    ai_review = response["choices"][0]["message"]["content"]
    return ai_review 
