def format_puzzle_text(text, max_chars_per_line=50, preserve_special=False):
    """
    Formata o texto do puzzle para caber na tela
    
    Args:
        text (str): Texto original
        max_chars_per_line (int): Número máximo de caracteres por linha
        preserve_special (bool): Se True, preserva caracteres especiais e formatação
        
    Returns:
        str: Texto formatado
    """
    if preserve_special and any(char in text for char in ['---', '\\', '|', '/']):
        return text
    
    # Remove espaços extras e quebras de linha
    text = ' '.join(text.split())
    
    words = text.split(' ')
    lines = []
    current_line = []
    current_length = 0
    
    for word in words:
        if current_length + len(word) + 1 > max_chars_per_line:
            if current_line:
                lines.append(' '.join(current_line))
            current_line = [word]
            current_length = len(word)
        else:
            current_line.append(word)
            current_length += len(word) + 1
    
    if current_line:
        lines.append(' '.join(current_line))
    
    return '\n'.join(lines) 