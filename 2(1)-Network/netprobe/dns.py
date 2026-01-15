from __future__ import annotations

import socket
from typing import Optional


def resolve(host: str) -> tuple[list[str], Optional[str]]:
    """
    도메인 이름을 IP 주소 리스트로 변환합니다.
    socket.getaddrinfo()을 사용해 DNS 해셕 결과를 받아오고, 결과에서 sockaddr[0]만 추출하여 IP 리스트를 구성합니다.
    조회된 IP 목록에서 중복을 제거하되 최초 등장 순서를 유지합니다.
    실패 시에는 예외 메시지를 error로 반환하며, IP 리스트는 빈 리스트로 반환합니다.

    Args:
    - host (str): 도메인 이름. 

    Returns:
    - tuple[list[str], Optional[str]]:
        - ips (list[str]): DNS 조회로 얻은 IP 주소 리스트
        - error (Optional[str]): 성공 시 None, 실패 시 예외 메시지 문자열.
    """
    try:
        infos = socket.getaddrinfo(host, None, proto=socket.IPPROTO_TCP)
        
        ###########################################################
        # TODO: sockaddr에서 IP 주소만 추출하여 리스트(ips)로 만드세요.
        # HINT: 리스트 컴프리헨션을 사용하여 sockaddr[0] 값을 가져오세요.

        ips = [sockaddr[0] for _, _, _, _, sockaddr in infos] # TODO: [이곳에 IP 리스트 생성 코드를 작성하세요]

        unique_ips = []
        seen = set()

        for ip in ips:
            if ip not in seen:
                seen.add(ip)
                unique_ips.append(ip)
        
        ips = unique_ips
        ###########################################################

        return ips, None
    except Exception as e:
        return [], str(e)


def pick_ip(ips: list[str], prefer: str = "any") -> Optional[str]:
    """
    주어진 IP 리스트 중 prefer 정책에 맞는 최적의 IP 하나를 선택하여 반환합니다. 
    
    요구사항:
    1. prefer가 "ipv4"인 경우: 리스트에서 가장 먼저 발견되는 IPv4 주소(:가 없는 주소)를 반환합니다. 
    2. prefer가 "ipv6"인 경우: 리스트에서 가장 먼저 발견되는 IPv6 주소(:가 있는 주소)를 반환합니다. 
    3. 정책에 맞는 주소가 없거나 prefer가 "any"인 경우: 리스트의 첫 번째 주소를 반환합니다. 

    Args:
    - ips (list[str]): DNS 조회로 얻은 IP 주소 리스트
    - prefer (str): prefer 정책으로 "any"(기본), "ipv4", "ipv6" 중 하나.

    Returns:
    - Optional[str]: prefer 정책에 맞게 선택된 IP 주소 문자열. 혹은 ips가 비어 있으면 None
    """
    if not ips:
        return None

    ###########################################################
    # TODO: prefer 정책에 따른 IP 선택 로직을 직접 구현하세요.
    # HINT: 리스트를 순회하며 조건문(if)으로 주소 형식을 검사해야 합니다.
    ###########################################################
    if prefer == "ipv4":
        for ip in ips:
            if ":" not in ip:
                return ip
                
    if prefer == "ipv6":
        for ip in ips:
            if ":" in ip:
                return ip

    return ips[0]