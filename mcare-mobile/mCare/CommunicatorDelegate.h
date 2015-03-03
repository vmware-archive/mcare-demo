//
//  CommunicatorDelegate.h
//  mCare
//
//  Created by Bob Webster on 12/14/14.
//  Copyright (c) 2014 vca. All rights reserved.
//

#ifndef mCare_CommunicatorDelegate_h
#define mCare_CommunicatorDelegate_h

@protocol CommunicatorDelegate
- (void)searchCSRReturnedData:(NSData *)objectNotation   withId:(NSString*) searchId;

- (void)searchCSRFailedWithError:(NSError *)error withId:(NSString *) searchId;
@end

#endif
