#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
部署翻譯補丁工具

自動複製 patches/ 目錄中的檔案到 Data/ 目錄，支援備份和還原功能。

使用方式:
    python deploy.py                    # 預設部署
    python deploy.py --backup           # 部署並備份原始檔案
    python deploy.py --restore          # 從備份還原
    python deploy.py --dry-run          # 預覽變更（不實際執行）
    python deploy.py --backup --dry-run # 預覽備份部署
"""

import os
import sys
import shutil
import argparse
import hashlib
from pathlib import Path
from datetime import datetime
from typing import List, Tuple

class DeployTool:
    def __init__(self, root_dir: Path = None):
        """初始化部署工具
        
        Args:
            root_dir: 專案根目錄，預設為腳本所在位置的上兩層
        """
        if root_dir is None:
            root_dir = Path(__file__).resolve().parent.parent.parent
        
        self.root_dir = root_dir
        self.patches_dir = root_dir / "patches"
        self.data_dir = root_dir / "Data"
        self.backup_dir = self.data_dir / "backup"
        
        # 支援的檔案格式
        self.allowed_extensions = {
            '.rxdata', '.dat', '.txt', '.json', '.xml', '.ini'
        }
    
    def validate_directories(self) -> bool:
        """驗證必要目錄是否存在"""
        if not self.patches_dir.exists():
            print(f"❌ 錯誤: patches 目錄不存在: {self.patches_dir}")
            return False
        
        if not self.data_dir.exists():
            print(f"❌ 錯誤: Data 目錄不存在: {self.data_dir}")
            return False
        
        return True
    
    def get_file_hash(self, file_path: Path) -> str:
        """計算檔案的 MD5 雜湊值"""
        hash_md5 = hashlib.md5()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    
    def validate_file_format(self, file_path: Path) -> bool:
        """驗證檔案格式是否允許"""
        if file_path.suffix.lower() in self.allowed_extensions:
            return True
        
        # .gitkeep 特殊處理
        if file_path.name == '.gitkeep':
            return False
        
        return False
    
    def get_files_to_deploy(self) -> List[Path]:
        """獲取所有需要部署的檔案"""
        files = []
        
        for file_path in self.patches_dir.rglob('*'):
            if file_path.is_file() and self.validate_file_format(file_path):
                files.append(file_path)
        
        return files
    
    def create_backup(self, target_file: Path, dry_run: bool = False) -> bool:
        """備份單個檔案
        
        Args:
            target_file: Data 目錄中的目標檔案
            dry_run: 是否為預覽模式
        
        Returns:
            備份是否成功（或在 dry_run 模式下是否可以成功）
        """
        if not target_file.exists():
            return True  # 目標檔案不存在，無需備份
        
        # 計算相對路徑
        relative_path = target_file.relative_to(self.data_dir)
        backup_file = self.backup_dir / relative_path
        
        if dry_run:
            print(f"  [DRY-RUN] 備份: {relative_path} -> backup/{relative_path}")
            return True
        
        # 創建備份目錄
        backup_file.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            shutil.copy2(target_file, backup_file)
            return True
        except Exception as e:
            print(f"❌ 備份失敗 {relative_path}: {e}")
            return False
    
    def deploy_file(self, source_file: Path, backup: bool = False, dry_run: bool = False) -> bool:
        """部署單個檔案
        
        Args:
            source_file: patches 目錄中的來源檔案
            backup: 是否備份現有檔案
            dry_run: 是否為預覽模式
        
        Returns:
            部署是否成功
        """
        # 計算目標路徑
        relative_path = source_file.relative_to(self.patches_dir)
        target_file = self.data_dir / relative_path
        
        # 備份現有檔案
        if backup and target_file.exists():
            if not self.create_backup(target_file, dry_run):
                return False
        
        if dry_run:
            if target_file.exists():
                print(f"  [DRY-RUN] 覆蓋: {relative_path}")
            else:
                print(f"  [DRY-RUN] 新增: {relative_path}")
            return True
        
        # 創建目標目錄
        target_file.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            shutil.copy2(source_file, target_file)
            return True
        except Exception as e:
            print(f"❌ 部署失敗 {relative_path}: {e}")
            return False
    
    def deploy(self, backup: bool = False, dry_run: bool = False, force: bool = False) -> bool:
        """執行部署
        
        Args:
            backup: 是否備份現有檔案
            dry_run: 是否為預覽模式
            force: 是否跳過確認
        
        Returns:
            部署是否成功
        """
        print("=" * 60)
        print("🚀 翻譯補丁部署工具")
        print("=" * 60)
        print()
        
        # 驗證目錄
        if not self.validate_directories():
            return False
        
        # 獲取要部署的檔案
        files = self.get_files_to_deploy()
        
        if not files:
            print("⚠️  警告: patches 目錄中沒有可部署的檔案")
            return False
        
        print(f"📦 找到 {len(files)} 個檔案待部署")
        print()
        
        # 檢查哪些檔案會被覆蓋
        existing_files = []
        new_files = []
        
        for source_file in files:
            relative_path = source_file.relative_to(self.patches_dir)
            target_file = self.data_dir / relative_path
            
            if target_file.exists():
                existing_files.append(relative_path)
            else:
                new_files.append(relative_path)
        
        # 顯示摘要
        if new_files:
            print(f"✨ 新增檔案: {len(new_files)}")
            if len(new_files) <= 10:
                for f in new_files:
                    print(f"   • {f}")
            print()
        
        if existing_files:
            print(f"⚠️  將覆蓋的檔案: {len(existing_files)}")
            if len(existing_files) <= 10:
                for f in existing_files:
                    print(f"   • {f}")
            elif not dry_run:
                print(f"   (顯示前 10 個)")
                for f in existing_files[:10]:
                    print(f"   • {f}")
            print()
        
        # 確認提示
        if not force and not dry_run and existing_files:
            print("⚠️  注意: 這將覆蓋現有檔案！")
            if backup:
                print(f"✅ 原始檔案將備份至: {self.backup_dir}")
            else:
                print("❌ 未啟用備份，覆蓋的檔案將無法還原！")
            print()
            
            response = input("確定要繼續嗎? (yes/no): ").strip().lower()
            if response not in ['yes', 'y', '是']:
                print("❌ 部署已取消")
                return False
            print()
        
        # 執行部署
        mode_str = "[預覽模式]" if dry_run else "[執行中]"
        if backup:
            mode_str += " [備份啟用]"
        
        print(f"{mode_str} 開始部署...")
        print()
        
        success_count = 0
        failed_count = 0
        
        for i, source_file in enumerate(files, 1):
            relative_path = source_file.relative_to(self.patches_dir)
            
            if not dry_run:
                print(f"[{i}/{len(files)}] 部署: {relative_path}")
            
            if self.deploy_file(source_file, backup, dry_run):
                success_count += 1
            else:
                failed_count += 1
        
        print()
        print("=" * 60)
        
        if dry_run:
            print("✅ 預覽完成")
            print(f"   • 將部署 {len(files)} 個檔案")
            print(f"   • 其中 {len(new_files)} 個新檔案, {len(existing_files)} 個覆蓋")
            if backup:
                print(f"   • 將備份 {len(existing_files)} 個現有檔案")
        else:
            print("✅ 部署完成")
            print(f"   • 成功: {success_count}")
            if failed_count > 0:
                print(f"   • 失敗: {failed_count}")
        
        print("=" * 60)
        
        return failed_count == 0
    
    def restore_from_backup(self, dry_run: bool = False, force: bool = False) -> bool:
        """從備份還原檔案
        
        Args:
            dry_run: 是否為預覽模式
            force: 是否跳過確認
        
        Returns:
            還原是否成功
        """
        print("=" * 60)
        print("♻️  從備份還原")
        print("=" * 60)
        print()
        
        if not self.backup_dir.exists():
            print(f"❌ 錯誤: 備份目錄不存在: {self.backup_dir}")
            return False
        
        # 獲取備份檔案
        backup_files = [f for f in self.backup_dir.rglob('*') if f.is_file()]
        
        if not backup_files:
            print("⚠️  警告: 備份目錄中沒有檔案")
            return False
        
        print(f"📦 找到 {len(backup_files)} 個備份檔案")
        
        if len(backup_files) <= 10:
            for backup_file in backup_files:
                relative_path = backup_file.relative_to(self.backup_dir)
                print(f"   • {relative_path}")
        
        print()
        
        # 確認提示
        if not force and not dry_run:
            print("⚠️  注意: 這將覆蓋當前的 Data 目錄檔案！")
            print()
            response = input("確定要還原嗎? (yes/no): ").strip().lower()
            if response not in ['yes', 'y', '是']:
                print("❌ 還原已取消")
                return False
            print()
        
        # 執行還原
        mode_str = "[預覽模式]" if dry_run else "[執行中]"
        print(f"{mode_str} 開始還原...")
        print()
        
        success_count = 0
        failed_count = 0
        
        for i, backup_file in enumerate(backup_files, 1):
            relative_path = backup_file.relative_to(self.backup_dir)
            target_file = self.data_dir / relative_path
            
            if dry_run:
                print(f"  [DRY-RUN] [{i}/{len(backup_files)}] 還原: {relative_path}")
                success_count += 1
            else:
                print(f"[{i}/{len(backup_files)}] 還原: {relative_path}")
                
                try:
                    target_file.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(backup_file, target_file)
                    success_count += 1
                except Exception as e:
                    print(f"❌ 還原失敗 {relative_path}: {e}")
                    failed_count += 1
        
        print()
        print("=" * 60)
        
        if dry_run:
            print("✅ 預覽完成")
            print(f"   • 將還原 {len(backup_files)} 個檔案")
        else:
            print("✅ 還原完成")
            print(f"   • 成功: {success_count}")
            if failed_count > 0:
                print(f"   • 失敗: {failed_count}")
        
        print("=" * 60)
        
        return failed_count == 0


def main():
    parser = argparse.ArgumentParser(
        description="翻譯補丁部署工具 - 自動複製 patches/ 到 Data/ 目錄",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
範例:
  python deploy.py                    # 預設部署
  python deploy.py --backup           # 部署並備份原始檔案
  python deploy.py --restore          # 從備份還原
  python deploy.py --dry-run          # 預覽變更
  python deploy.py --backup --dry-run # 預覽備份部署
  python deploy.py --force            # 跳過確認提示
        """
    )
    
    parser.add_argument(
        '--backup',
        action='store_true',
        help='在覆蓋前備份原始檔案到 Data/backup/'
    )
    
    parser.add_argument(
        '--restore',
        action='store_true',
        help='從 Data/backup/ 還原備份檔案'
    )
    
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='預覽變更，不實際執行操作'
    )
    
    parser.add_argument(
        '--force',
        action='store_true',
        help='跳過確認提示，直接執行'
    )
    
    args = parser.parse_args()
    
    # 創建部署工具實例
    deploy_tool = DeployTool()
    
    try:
        if args.restore:
            # 還原模式
            success = deploy_tool.restore_from_backup(
                dry_run=args.dry_run,
                force=args.force
            )
        else:
            # 部署模式
            success = deploy_tool.deploy(
                backup=args.backup,
                dry_run=args.dry_run,
                force=args.force
            )
        
        sys.exit(0 if success else 1)
    
    except KeyboardInterrupt:
        print("\n\n❌ 操作已中斷")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ 發生錯誤: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
