import re

log_data = """

"""

def parse_line(line):
    pattern = (
        r'Wr:\s*(\d+)\s*\|\s*Rd:\s*(\d+)\s*\|\s*Din:\s*(0x[0-9a-fA-F]+)\s*\|\s*'
        r'Dout:\s*(0x[0-9a-fA-F]+)\s*\|\s*Wr_Ptr:\s*(0x[0-9a-fA-F]+)\s*\(wrap:(\d+)\)\s*\|\s*'
        r'Rd_Ptr:\s*(0x[0-9a-fA-F]+)\s*\(wrap:(\d+)\)\s*\|\s*Count:\s*(\d+)\s*\|\s*'
        r'Full:\s*(\d+)\s*\|\s*Empty:\s*(\d+)'
    )
    match = re.search(pattern, line)
    if not match:
        return None
    g = match.groups()
    return {
        'Wr': int(g[0]),
        'Rd': int(g[1]),
        'Wr_Ptr': int(g[4], 16),
        'Wr_wrap': int(g[5]),
        'Rd_Ptr': int(g[6], 16),
        'Rd_wrap': int(g[7]),
        'Count': int(g[8]),
        'Full': int(g[9]),
        'Empty': int(g[10])
    }

def advance_ptr(ptr, wrap):
    ptr += 1
    if ptr > 0xF:
        ptr = 0
        wrap = 1 - wrap
    return ptr, wrap

def verify_fifo_same_line(log_text):
    lines = [l.strip() for l in log_text.strip().split('\n') if l]
    parsed = [parse_line(l) for l in lines if parse_line(l)]
    
    if not parsed:
        print("Brak danych do weryfikacji.")
        return

    errors = 0
    prev_state = parsed[0]
    
    for idx in range(1, len(parsed)):
        curr = parsed[idx]
        
        wr = curr['Wr']
        rd = curr['Rd']
        full_prev = prev_state['Full']
        empty_prev = prev_state['Empty']
        
        exp_count = prev_state['Count']
        exp_wr_ptr = prev_state['Wr_Ptr']
        exp_wr_wrap = prev_state['Wr_wrap']
        exp_rd_ptr = prev_state['Rd_Ptr']
        exp_rd_wrap = prev_state['Rd_wrap']
        
        # Niezależna ocena powodzenia zapisu i odczytu uwzględniająca stan Full/Empty
        write_success = (wr == 1) and not (full_prev == 1)
        read_success = (rd == 1) and not (empty_prev == 1)
        
        if write_success:
            exp_count += 1
            exp_wr_ptr, exp_wr_wrap = advance_ptr(exp_wr_ptr, exp_wr_wrap)
            
        if read_success:
            exp_count -= 1
            exp_rd_ptr, exp_rd_wrap = advance_ptr(exp_rd_ptr, exp_rd_wrap)

        # Weryfikacja zgodności pól "po" w tej samej linijce
        mismatches = []
        if curr['Count'] != exp_count:
            mismatches.append(f"Count: oczekiwano {exp_count}, otrzymano {curr['Count']}")
        if curr['Wr_Ptr'] != exp_wr_ptr or curr['Wr_wrap'] != exp_wr_wrap:
            mismatches.append(f"Wr_Ptr: oczekiwano 0x{exp_wr_ptr:x}(wrap:{exp_wr_wrap}), otrzymano 0x{curr['Wr_Ptr']:x}(wrap:{curr['Wr_wrap']})")
        if curr['Rd_Ptr'] != exp_rd_ptr or curr['Rd_wrap'] != exp_rd_wrap:
            mismatches.append(f"Rd_Ptr: oczekiwano 0x{exp_rd_ptr:x}(wrap:{exp_rd_wrap}), otrzymano 0x{curr['Rd_Ptr']:x}(wrap:{curr['Rd_wrap']})")

        if mismatches:
            errors += 1
            print(f"Błąd w linijce {idx + 1} [Wr: {wr}, Rd: {rd}]:")
            for m in mismatches:
                print(f"  - {m}")
        
        prev_state = curr

    if errors == 0:
        print("Wszystkie linie są poprawne!")
    else:
        print(f"Znaleziono błędnych linii: {errors}")

if __name__ == "__main__":
    verify_fifo_same_line(log_data)
