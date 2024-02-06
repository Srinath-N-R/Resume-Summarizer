def generate_summary(name, organization, education):
    """
    Generates a summary from the extracted resume information.

    :param name: The name of the person.
    :param organization: Organization associated with the person as a single entity.
    :param education: A list of education details associated with the person.
    :return: A string containing the generated summary.
    """
    summary = f"{name} has been associated with {organization}. "  # Modify this line
    summary += f"Their educational background includes {'; '.join(education)}. "
    summary += "This diverse experience and educational background suggest a well-rounded and versatile professional."

    return summary
