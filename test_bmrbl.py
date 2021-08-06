import pytest
import test_parser as parser
from enum import Enum
from pathlib import Path
import os


#-------------------------------------------------------------------------------
dummy_app_img_s = next(Path(os.getcwd()).parent.parent.rglob('dummy_app_S_img'))
dummy_app_img_m = next(Path(os.getcwd()).parent.parent.rglob('dummy_app_M_img'))
dummy_app_info_img_s = next(Path(os.getcwd()).parent.parent.rglob('dummy_app_S_info_img'))
dummy_app_info_img_m = next(Path(os.getcwd()).parent.parent.rglob('dummy_app_M_info_img'))


#-------------------------------------------------------------------------------
class OTP_Fuse(Enum):
    MBIST                               = 0,
    JTAG                                = 1,
    SILENT_BOOT                         = 2,
    SECURE_BOOT_ONLY                    = 3,
    UART_BOOT_ABORT_DISABLED            = 4,
    GPIO_BOOT_MODE_DISABLED             = 5,
    M_MODE_BOOT_DISABLED                = 6,
    ROM_SEL4_BOOT_ONLY                  = 7,
    UART_LOADER_SRAM_M_MODE_DISABLED    = 8,
    UART_LOADER_SRAM_DISABLED           = 9,
    UART_LOADER_FLASH_UPDATE_DISABLED   = 10,
    SOFT_OTP                            = 11,
    LOCK_OTP_FEATURE_FLAGS              = 12,
    LOCK_OTP_USER                       = 13,


#-------------------------------------------------------------------------------
class MemProvisioningCtx:
    def __init__(
        self,
        kernel_bin=None,
        kernel_addr=0x80200000,
        root_task_bin=None,
        root_task_addr=None,
        info_block_bin=None,
        info_block_addr=0x803fe800,
        otp_reg_addr_low=0x88000000,
        otp_reg_addr_high=0x88000004,
        otp_reg_value_low=None,
        otp_reg_value_high=None):

        self.kernel_bin = kernel_bin
        self.kernel_addr = kernel_addr
        self.root_task_bin = root_task_bin
        self.root_task_addr = root_task_addr
        self.info_block_bin = info_block_bin
        self.info_block_addr = info_block_addr
        self.otp_reg_addr_low = otp_reg_addr_low
        self.otp_reg_addr_high = otp_reg_addr_high
        self.otp_reg_value_low = otp_reg_value_low
        self.otp_reg_value_high = otp_reg_value_high


#-------------------------------------------------------------------------------
def blow_fuses(fuses_to_blow):
    otp_reg = ['1' for idx in range(32)]

    for fuse in fuses_to_blow:
        otp_reg[len(otp_reg) - 1 - fuse.value[0]] = '0'

    return hex(int(''.join(otp_reg), 2))


#-------------------------------------------------------------------------------
otp_reg_all_permitted = blow_fuses([])
otp_reg_sel4_only = blow_fuses([OTP_Fuse.ROM_SEL4_BOOT_ONLY])
otp_reg_m_mode_disabled = blow_fuses([OTP_Fuse.M_MODE_BOOT_DISABLED])
otp_reg_uart_disabled = blow_fuses([OTP_Fuse.UART_BOOT_ABORT_DISABLED])
otp_reg_gpio_disabled = blow_fuses([OTP_Fuse.GPIO_BOOT_MODE_DISABLED])

otp_reg_m_mode_disabled_no_uart_selection = blow_fuses([
    OTP_Fuse.M_MODE_BOOT_DISABLED,
    OTP_Fuse.UART_BOOT_ABORT_DISABLED])

otp_reg_sel4_only_no_uart_selection = blow_fuses([
    OTP_Fuse.ROM_SEL4_BOOT_ONLY,
    OTP_Fuse.UART_BOOT_ABORT_DISABLED])

otp_reg_gpio_and_uart_disabled = blow_fuses([
    OTP_Fuse.UART_BOOT_ABORT_DISABLED,
    OTP_Fuse.GPIO_BOOT_MODE_DISABLED])

otp_reg_loader_and_uart_disabled = blow_fuses([
    OTP_Fuse.UART_BOOT_ABORT_DISABLED,
    OTP_Fuse.UART_LOADER_SRAM_M_MODE_DISABLED,
    OTP_Fuse.UART_LOADER_SRAM_DISABLED,
    OTP_Fuse.UART_LOADER_FLASH_UPDATE_DISABLED])

otp_reg_loader_gpio_and_uart_disabled = blow_fuses([
    OTP_Fuse.UART_BOOT_ABORT_DISABLED,
    OTP_Fuse.GPIO_BOOT_MODE_DISABLED,
    OTP_Fuse.UART_LOADER_SRAM_M_MODE_DISABLED,
    OTP_Fuse.UART_LOADER_SRAM_DISABLED,
    OTP_Fuse.UART_LOADER_FLASH_UPDATE_DISABLED])

#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
@pytest.mark.parametrize(
    'mem_provisioning_ctx',
    [MemProvisioningCtx(
        otp_reg_value_low='{}'.format(otp_reg_all_permitted),
        otp_reg_value_high='{}'.format(otp_reg_all_permitted)
    ),
    MemProvisioningCtx(
        otp_reg_value_low='{}'.format(otp_reg_gpio_disabled),
        otp_reg_value_high='{}'.format(otp_reg_all_permitted)
    )])
def test_simple_boot(boot_bootloader):
    """
    1.  Test that checks if the bmrbl loads correctly, fails flash boot and
        displays the boot menu.

        - No pre-provisioned memory content
        - No OTP fuses blown


    2.  Test that checks if the bmrbl loads correctly, defaults to flash boot
        since the GPIO boot selection is disabled, fails and displays the boot
        menu.

        - No pre-provisioned memory content
        - OTP fuses blown
            - GPIO_BOOT_MODE_DISABLED
    """

    test_runner = boot_bootloader()[0]

    (ret , idx, idx2) = test_runner.system_log_match_multiple_sequences([

        ( [ 'HENSOLDT Cyber GmbH' ], 5 ),
        ( [ "ERROR: can't boot from Flash configuration" ], 5 ),
        ( [ 'boot options:' ], 5 ),
        ( [ 'Choose mode:' ], 5 )
    ])

    if not ret:
        pytest.fail('boot string #{}.{} not found'.format(idx, idx2))


#-------------------------------------------------------------------------------
@pytest.mark.parametrize(
    'mem_provisioning_ctx',
    [MemProvisioningCtx(
        otp_reg_value_low='{}'.format(otp_reg_uart_disabled),
        otp_reg_value_high='{}'.format(otp_reg_all_permitted)
    ),
    MemProvisioningCtx(
        otp_reg_value_low='{}'.format(otp_reg_gpio_and_uart_disabled),
        otp_reg_value_high='{}'.format(otp_reg_all_permitted)
    )])
def test_simple_boot_no_uart_selection(boot_bootloader):
    """
    1.  Test that checks if the bmrbl loads, fails flash boot and starts the
        secure loader since UART selection is disabled.

        - No pre-provisioned memory content
        - OTP fuses blown
            - UART_BOOT_ABORT_DISABLED


    2.  Test that checks if the bmrbl loads correctly, defaults to flash boot
        since the GPIO boot selection is disabled, fails and runs the secure
        loader since UART selection is disabled.

        - No pre-provisioned memory content
        - OTP fuses blown
            - GPIO_BOOT_MODE_DISABLED
            - UART_BOOT_ABORT_DISABLED
    """

    test_runner = boot_bootloader()[0]

    (ret , idx, idx2) = test_runner.system_log_match_multiple_sequences([

        ( [ 'HENSOLDT Cyber GmbH' ], 5 ),
        ( [ "ERROR: can't boot from Flash configuration" ], 5 ),
        ( [ 'loader ready for input' ], 5 )
    ])

    if not ret:
        pytest.fail('boot string #{}.{} not found'.format(idx, idx2))


#-------------------------------------------------------------------------------
@pytest.mark.parametrize(
    'mem_provisioning_ctx',
    [MemProvisioningCtx(
        otp_reg_value_low='{}'.format(otp_reg_loader_and_uart_disabled),
        otp_reg_value_high='{}'.format(otp_reg_all_permitted)
    ),
    MemProvisioningCtx(
        otp_reg_value_low='{}'.format(otp_reg_loader_and_uart_disabled),
        otp_reg_value_high='{}'.format(otp_reg_all_permitted)
    )])
def test_simple_boot_no_uart_selection_no_loader(boot_bootloader):
    """
    1.  Test that checks if the bmrbl loads, fails flash boot and halts since
        UART selection and secure loader are disabled.

        - No pre-provisioned memory content
        - OTP fuses blown
            - UART_BOOT_ABORT_DISABLED
            - UART_LOADER_SRAM_M_MODE_DISABLED
            - UART_LOADER_SRAM_DISABLED
            - UART_LOADER_FLASH_UPDATE_DISABLED

    2.  Test that checks if the bmrbl loads, defaults to flash load since GPIO
        is disabled, fails flash boot and halts since UART selection and secure
        loader are disabled.

        - No pre-provisioned memory content
        - OTP fuses blown
            - UART_BOOT_ABORT_DISABLED
            - GPIO_BOOT_MODE_DISABLED
            - UART_LOADER_SRAM_M_MODE_DISABLED
            - UART_LOADER_SRAM_DISABLED
            - UART_LOADER_FLASH_UPDATE_DISABLED
    """

    test_runner = boot_bootloader()[0]

    (ret , idx, idx2) = test_runner.system_log_match_multiple_sequences([

        ( [ 'HENSOLDT Cyber GmbH' ], 5 ),
        ( [ "ERROR: can't boot from Flash configuration" ], 5 ),
        ( [ 'ERROR: invalid boot mode, UART loader not allowed' ], 5 )
    ])

    if not ret:
        pytest.fail('boot string #{}.{} not found'.format(idx, idx2))


#-------------------------------------------------------------------------------
@pytest.mark.parametrize(
    'mem_provisioning_ctx',
    [MemProvisioningCtx(
        info_block_bin=dummy_app_info_img_s,
        otp_reg_value_low='{}'.format(otp_reg_all_permitted),
        otp_reg_value_high='{}'.format(otp_reg_all_permitted)
    )])
def test_bmrbl_info_block_no_kernel(boot_bootloader):
    """
    Test that checks if the bmrbl loads correctly, reads the info block
    correctly, tries to boot the image from flash, fails and prints the boot
    menu.

    - Info block in memory
    - No OTP fuses blown
    """

    test_runner = boot_bootloader()[0]

    (ret , idx, idx2) = test_runner.system_log_match_multiple_sequences([

        ( [ 'HENSOLDT Cyber GmbH' ], 5 ),
        ( [ '0x4853414c462d4249' ], 5 ),
        ( [ 'checking integrity of Flash info block' ], 5 ),
        ( [ 'Trying to boot an image from flash...' ], 5 ),
        ( [ "ERROR: can't boot from Flash configuration" ], 5 ),
        ( [ 'boot options:' ], 5 ),
        ( [ 'Choose mode:' ], 5 )

    ])

    if not ret:
        pytest.fail('boot string #{}.{} not found'.format(idx, idx2))


#-------------------------------------------------------------------------------
@pytest.mark.parametrize(
    'mem_provisioning_ctx',
    [MemProvisioningCtx(
        kernel_bin=dummy_app_img_s,
        info_block_bin=dummy_app_info_img_s,
        otp_reg_value_low='{}'.format(otp_reg_all_permitted),
        otp_reg_value_high='{}'.format(otp_reg_all_permitted)
    )])
def test_bmrbl_info_block_and_kernel(boot_bootloader):
    """
    Test that checks if the bmrbl loads correctly, reads the info block
    correctly and successfully boots the image from flash in S mode.

    - Info block and kernel in memory
    - No OTP fuses blown
    """

    test_runner = boot_bootloader()[0]

    (ret , idx, idx2) = test_runner.system_log_match_multiple_sequences([

        ( [ 'HENSOLDT Cyber GmbH' ], 5 ),
        ( [ '0x4853414c462d4249' ], 5 ),
        ( [ 'checking integrity of Flash info block' ], 5 ),
        ( [ 'hand over to S-Mode at' ], 5 ),
        ( [ "Second stage Flash Bootloader" ], 5 ),

    ])

    if not ret:
        pytest.fail('boot string #{}.{} not found'.format(idx, idx2))


#-------------------------------------------------------------------------------
@pytest.mark.parametrize(
    'mem_provisioning_ctx',
    [MemProvisioningCtx(
        kernel_bin=dummy_app_img_s,
        info_block_bin=dummy_app_info_img_s,
        otp_reg_value_low='{}'.format(otp_reg_sel4_only),
        otp_reg_value_high='{}'.format(otp_reg_all_permitted)
    )])
def test_bmrbl_info_block_and_kernel_only_sel4_allowed(boot_bootloader):
    """
    Test that checks if the bmrbl loads correctly, reads the info block
    correctly but does not boot the image from flash since only sel4 systems are
    allowed.

    - Info block and kernel in memory
    - OTP fuses blown:
        - ROM_SEL4_BOOT_ONLY
    """

    test_runner = boot_bootloader()[0]

    (ret , idx, idx2) = test_runner.system_log_match_multiple_sequences([

        ( [ 'HENSOLDT Cyber GmbH' ], 5 ),
        ( [ '0x4853414c462d4249' ], 5 ),
        ( [ 'checking integrity of Flash info block' ], 5 ),
        ( [ 'ERROR: invalid boot mode 1, only seL4 system boot allowed' ], 5 ),
        ( [ 'boot options:' ], 5 ),
        ( [ 'Choose mode:' ], 5 )

    ])

    if not ret:
        pytest.fail('boot string #{}.{} not found'.format(idx, idx2))


#-------------------------------------------------------------------------------
@pytest.mark.parametrize(
    'mem_provisioning_ctx',
    [MemProvisioningCtx(
        kernel_bin=dummy_app_img_s,
        info_block_bin=dummy_app_info_img_s,
        otp_reg_value_low='{}'.format(otp_reg_sel4_only_no_uart_selection),
        otp_reg_value_high='{}'.format(otp_reg_all_permitted)
    )])
def test_bmrbl_info_block_and_kernel_only_sel4_allowed_2(boot_bootloader):
    """
    Test that checks if the bmrbl loads correctly, reads the info block
    correctly but does not boot the image from flash since only sel4 systems are
    allowed.

    - Info block and kernel in memory
    - OTP fuses blown:
        - ROM_SEL4_BOOT_ONLY
        - UART_BOOT_ABORT_DISABLED
    """

    test_runner = boot_bootloader()[0]

    (ret , idx, idx2) = test_runner.system_log_match_multiple_sequences([

        ( [ 'HENSOLDT Cyber GmbH' ], 5 ),
        ( [ '0x4853414c462d4249' ], 5 ),
        ( [ 'checking integrity of Flash info block' ], 5 ),
        ( [ 'ERROR: invalid boot mode 1, only seL4 system boot allowed' ], 5 ),
        ( [ 'loader ready for input' ], 5 )

    ])

    if not ret:
        pytest.fail('boot string #{}.{} not found'.format(idx, idx2))


#-------------------------------------------------------------------------------
@pytest.mark.parametrize(
    'mem_provisioning_ctx',
    [MemProvisioningCtx(
        kernel_bin=dummy_app_img_m,
        info_block_bin=dummy_app_info_img_m,
        otp_reg_value_low='{}'.format(otp_reg_m_mode_disabled),
        otp_reg_value_high='{}'.format(otp_reg_all_permitted)
    )])
def test_bmrbl_info_block_and_kernel_m_mode_disabled(boot_bootloader):
    """
    Test that checks if the bmrbl loads correctly, reads the info block with
    M-Mode selected correctly but does not boot the image from flash since only
    S-Mode is allowed.

    - Info block and kernel in memory
    - OTP fuses blown:
        - M_MODE_BOOT_DISABLED
    """

    test_runner = boot_bootloader()[0]

    (ret , idx, idx2) = test_runner.system_log_match_multiple_sequences([

        ( [ 'HENSOLDT Cyber GmbH' ], 5 ),
        ( [ '0x4853414c462d4249' ], 5 ),
        ( [ 'mode:                       2' ], 5 ),
        ( [ 'checking integrity of Flash info block' ], 5 ),
        ( [ 'ERROR: invalid boot mode 2, only S-Mode allowed' ], 5 ),
        ( [ "ERROR: can't boot from Flash configuration" ], 5 ),
        ( [ 'boot options:' ], 5 )

    ])

    if not ret:
        pytest.fail('boot string #{}.{} not found'.format(idx, idx2))


#-------------------------------------------------------------------------------
@pytest.mark.parametrize(
    'mem_provisioning_ctx',
    [MemProvisioningCtx(
        kernel_bin=dummy_app_img_m,
        info_block_bin=dummy_app_info_img_m,
        otp_reg_value_low='{}'.format(otp_reg_m_mode_disabled_no_uart_selection),
        otp_reg_value_high='{}'.format(otp_reg_all_permitted)
    )])
def test_bmrbl_info_block_and_kernel_m_mode_disabled_2(boot_bootloader):
    """
    Test that checks if the bmrbl loads correctly, reads the info block with
    M-Mode selected correctly but does not boot the image from flash since only
    S-Mode is allowed.

    - Info block and kernel in memory
    - OTP fuses blown:
        - M_MODE_BOOT_DISABLED
        - UART_BOOT_ABORT_DISABLED
    """

    test_runner = boot_bootloader()[0]

    (ret , idx, idx2) = test_runner.system_log_match_multiple_sequences([

        ( [ 'HENSOLDT Cyber GmbH' ], 5 ),
        ( [ '0x4853414c462d4249' ], 5 ),
        ( [ 'mode:                       2' ], 5 ),
        ( [ 'checking integrity of Flash info block' ], 5 ),
        ( [ 'ERROR: invalid boot mode 2, only S-Mode allowed' ], 5 ),
        ( [ "ERROR: can't boot from Flash configuration" ], 5 ),
        ( [ 'loader ready for input' ], 5 )

    ])

    if not ret:
        pytest.fail('boot string #{}.{} not found'.format(idx, idx2))