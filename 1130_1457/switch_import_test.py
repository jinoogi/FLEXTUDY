import switches_lgpio
import time

try:
    # GPIO 설정 초기화
    switches_lgpio.setup_gpio()

    print("스위치 상태 감지 시작. Ctrl+C로 종료합니다.")
    while True:
        time.sleep(1)  # 루프 유지

except KeyboardInterrupt:
    print("프로그램 종료 중...")

finally:
    # GPIO 설정 정리
    switches_lgpio.cleanup_gpio()
