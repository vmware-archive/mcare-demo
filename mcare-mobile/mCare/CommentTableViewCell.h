//
//  CommentCellTableViewCell.h
//  mCare
//
//  Created by Bob Webster on 1/6/15.
//  Copyright (c) 2015 vca. All rights reserved.
//

#import <UIKit/UIKit.h>

@interface CommentTableViewCell : UITableViewCell

@property (nonatomic, weak) IBOutlet UILabel *headerLabel;
@property (nonatomic, weak) IBOutlet UILabel *headerRightLabel;
@property (nonatomic, weak) IBOutlet UILabel *bodyLabel;

@end
